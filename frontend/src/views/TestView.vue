<!--
  TestView.vue —— NPFJ 动态路由答题页
  每个题池固定 5 题，四选一，不暴露任何路由/权重信息给前端。
  颜色随阶段渐变：蓝 → 青 → 紫 → 粉
-->
<template>
  <div class="test-page" :style="{ '--accent': accentColor, '--accent2': accentColor2, '--accent-glow': accentGlow }">
    <!-- 动态渐变背景层 -->
    <div class="bg-layer" :style="{ background: bgGradient }"></div>

    <!-- 顶部：阶段指示 -->
    <div class="stage-header">
      <div class="stage-badge" v-if="poolInfo">阶段 {{ poolInfo.stage }} / 4</div>
      <div class="pool-name" v-if="poolInfo">{{ poolInfo.name }}</div>
      <div class="pool-desc" v-if="poolInfo">{{ poolInfo.description }}</div>
      <div class="path-dots">
        <span v-for="(step, i) in pathSteps" :key="i" class="pdot"
          :class="{ filled: step.done, current: step.active }"
          :style="step.done ? { background: accentColor } : {}"
        ></span>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner" :style="{ borderTopColor: accentColor }"></div>
      <p>加载中...</p>
    </div>

    <template v-if="!loading && currentQuestions.length > 0">
      <div class="q-area">
        <h2 class="q-text">{{ currentQuestion.text }}</h2>
        <div class="options">
          <div v-for="opt in currentQuestion.options" :key="opt.key"
            class="option"
            :class="{ selected: selectedAnswer === opt.key }"
            :style="selectedAnswer === opt.key ? { borderColor: accentColor, background: accentColor + '22' } : {}"
            @click="selectOption(opt.key)"
          >
            <span class="opt-key" :style="selectedAnswer === opt.key ? { background: accentColor } : {}">{{ opt.key }}</span>
            <span class="opt-text">{{ opt.text }}</span>
          </div>
        </div>
      </div>

      <button class="next-btn" :disabled="!selectedAnswer"
        :style="selectedAnswer ? { background: `linear-gradient(135deg, ${accentColor}, ${accentColor2})` } : {}"
        @click="nextQuestion">
        {{ isLastQuestion ? '提交本组' : '下一题' }}
      </button>
    </template>

    <div v-if="submitting" class="loading-overlay">
      <div class="spinner" :style="{ borderTopColor: accentColor }"></div>
      <p>分析中...</p>
    </div>
    <div v-if="errorMsg" class="error-toast">{{ errorMsg }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createSession, getPool, submitPool, getResult } from '../api/request.js'

const router = useRouter()
const sessionId = ref(null)
const poolId = ref(1)
const poolInfo = ref(null)
const currentQuestions = ref([])
const currentQIndex = ref(0)
const answers = ref([])
const selectedAnswer = ref(null)
const pathSteps = ref([])
const loading = ref(true)
const submitting = ref(false)
const errorMsg = ref('')

// 各阶段配色方案
const stageColors = [
  { accent: '#4facfe', accent2: '#667eea', glow: 'rgba(79,172,254,0.15)', bg: 'radial-gradient(ellipse at 30% 20%, rgba(79,172,254,0.08) 0%, transparent 60%)' },
  { accent: '#00d2ff', accent2: '#3a7bd5', glow: 'rgba(0,210,255,0.15)', bg: 'radial-gradient(ellipse at 50% 30%, rgba(0,210,255,0.06) 0%, transparent 60%)' },
  { accent: '#a855f7', accent2: '#7c3aed', glow: 'rgba(168,85,247,0.15)', bg: 'radial-gradient(ellipse at 40% 20%, rgba(168,85,247,0.06) 0%, transparent 60%)' },
  { accent: '#f472b6', accent2: '#ec4899', glow: 'rgba(244,114,182,0.15)', bg: 'radial-gradient(ellipse at 60% 30%, rgba(244,114,182,0.06) 0%, transparent 60%)' },
]

const currentStage = computed(() => Math.max(0, (poolInfo.value?.stage || 1) - 1))
const accentColor = computed(() => stageColors[currentStage.value]?.accent || '#4facfe')
const accentColor2 = computed(() => stageColors[currentStage.value]?.accent2 || '#667eea')
const accentGlow = computed(() => stageColors[currentStage.value]?.glow || 'rgba(79,172,254,0.15)')
const bgGradient = computed(() => stageColors[currentStage.value]?.bg || '')

const currentQuestion = computed(() => currentQuestions.value[currentQIndex.value] || {})
const answeredCount = computed(() => answers.value.filter(a => a !== undefined).length)
const isLastQuestion = computed(() => currentQIndex.value === currentQuestions.value.length - 1)

onMounted(async () => {
  try {
    const r = await createSession()
    sessionId.value = r.data.session_id
    await loadPool(r.data.first_pool)
  } catch { errorMsg.value = '⚠️ 后端未连接'; loading.value = false }
})

async function loadPool(id) {
  loading.value = true
  try {
    const r = await getPool(id)
    const d = r.data
    poolId.value = d.id
    poolInfo.value = { stage: d.stage, name: d.name, description: d.description }
    currentQuestions.value = d.questions
    currentQIndex.value = 0
    answers.value = []
    selectedAnswer.value = null
    updatePathDots(d.stage)
  } catch { errorMsg.value = '⚠️ 加载失败' }
  loading.value = false
}

function updatePathDots(stage) {
  const dots = []
  const labels = ['能量', '参与', '认知', '表达']
  for (let i = 0; i < 4; i++) {
    dots.push({ done: i < stage, active: i === stage })
  }
  pathSteps.value = dots
}

function selectOption(key) { selectedAnswer.value = key }

function nextQuestion() {
  if (!selectedAnswer.value) return
  answers.value[currentQIndex.value] = selectedAnswer.value
  if (!isLastQuestion.value) {
    currentQIndex.value++
    selectedAnswer.value = null
    return
  }
  submitCurrentPool()
}

async function submitCurrentPool() {
  submitting.value = true
  try {
    const r = await submitPool(poolId.value, answers.value)
    if (r.data.is_final) {
      const rr = await getResult()
      router.push({ name: 'Result', query: { data: JSON.stringify(rr.data) } })
    } else if (r.data.next_pool) {
      await loadPool(r.data.next_pool)
    }
  } catch { errorMsg.value = '⚠️ 提交失败' }
  submitting.value = false
}
</script>

<style scoped>
.test-page {
  max-width: 560px; margin: 0 auto; padding: 30px 20px;
  min-height: 100vh; display: flex; flex-direction: column;
  position: relative; transition: --accent 0.6s ease;
}
.bg-layer {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  pointer-events: none; transition: all 0.8s ease; z-index: 0;
}

.stage-header {
  text-align: center; margin-bottom: 24px; position: relative; z-index: 1;
}
.stage-badge {
  display: inline-block; background: var(--accent-glow, rgba(79,172,254,0.12));
  border: 1px solid color-mix(in srgb, var(--accent, #4facfe) 30%, transparent);
  padding: 4px 14px; border-radius: 12px; font-size: 12px; letter-spacing: 2px; margin-bottom: 10px;
  color: var(--accent, #4facfe);
}
.pool-name { font-size: 20px; font-weight: 700; margin-bottom: 4px; }
.pool-desc { font-size: 13px; color: rgba(255,255,255,0.45); margin-bottom: 14px; }

/* 路径点指示器 */
.path-dots { display: flex; justify-content: center; gap: 10px; }
.pdot {
  width: 10px; height: 10px; border-radius: 50%;
  background: rgba(255,255,255,0.12); transition: all 0.4s ease;
}
.pdot.current { box-shadow: 0 0 10px var(--accent-glow, rgba(79,172,254,0.3)); transform: scale(1.3); }
.pdot.filled { background: var(--accent, #4facfe); }

/* 题目区 */
.q-area { flex: 1; position: relative; z-index: 1; display: flex; flex-direction: column; justify-content: center; }
.q-text {
  font-size: 20px; line-height: 1.6; margin-bottom: 24px; text-align: center; font-weight: 500;
}
.options { display: flex; flex-direction: column; gap: 10px; }
.option {
  display: flex; align-items: center; gap: 14px; padding: 14px 16px;
  background: rgba(255,255,255,0.04); border: 1.5px solid rgba(255,255,255,0.08);
  border-radius: 12px; cursor: pointer; transition: all 0.2s ease;
}
.option:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.18); }
.option.selected { background: var(--accent-glow, rgba(79,172,254,0.08)); }
.opt-key {
  width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;
  background: rgba(255,255,255,0.08); border-radius: 50%; font-weight: 700; font-size: 13px;
  flex-shrink: 0; transition: background 0.2s;
}
.opt-text { font-size: 15px; line-height: 1.4; }

/* 按钮 */
.next-btn {
  width: 100%; padding: 14px; border: none; border-radius: 12px;
  font-size: 16px; color: #fff; cursor: pointer; transition: all 0.2s;
  position: relative; z-index: 1; margin-top: 20px;
  background: rgba(255,255,255,0.08);
}
.next-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.next-btn:not(:disabled):hover { transform: translateY(-1px); box-shadow: 0 6px 20px var(--accent-glow, rgba(79,172,254,0.2)); }

/* 加载动画 */
.loading-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15,12,41,0.9); display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 16px; z-index: 100;
}
.loading-state { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 300px; gap: 12px; color: rgba(255,255,255,0.5); position: relative; z-index: 1; }
.spinner { width: 36px; height: 36px; border: 3px solid rgba(255,255,255,0.08); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.error-toast {
  position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
  background: rgba(255, 107, 107, 0.9); color: #fff; padding: 10px 20px;
  border-radius: 8px; font-size: 13px; z-index: 200;
}
</style>
