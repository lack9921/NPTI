<!--
  TestView.vue —— NPFJ 动态路由答题页
  使用 Naive UI 组件
-->
<template>
  <div class="test-page" :style="{ '--accent': accentColor, '--accent2': accentColor2 }">
    <div class="bg-layer" :style="{ background: pageBg }"></div>
    <div class="glow-layer" :style="{ background: bgGlow }"></div>

    <div class="stage-header">
      <n-tag :bordered="false" size="small" :style="{ background: accentColor + '18', color: accentColor, border: 'none', fontWeight: 600, letterSpacing: '1px' }">
        阶段 {{ poolInfo?.stage }} / 4
      </n-tag>
      <div class="pool-name">{{ poolInfo?.name }}</div>
      <div class="pool-desc">{{ poolInfo?.description }}</div>
      <div class="q-ref" v-if="currentQuestion.id">#{{ currentQuestion.id }} · Pool {{ poolId }}</div>

      <n-steps :current="currentStepIndex" :status="'process'" size="small" class="steps-bar">
        <n-step title="能量" />
        <n-step title="参与" />
        <n-step title="认知" />
        <n-step title="表达" />
      </n-steps>
    </div>

    <div v-if="loading" class="loading-state">
      <n-spin size="medium" />
      <p>加载中...</p>
    </div>

    <template v-if="!loading && currentQuestions.length > 0">
      <div class="q-area">
        <div class="q-progress-text">{{ answeredCount }} / 5</div>
        <n-progress type="line" :percentage="answeredCount * 20" :border-radius="3" :height="5"
          :color="accentColor" :rail-color="'rgba(255,255,255,0.06)'" :show-indicator="false"
          class="q-progress" />

        <h2 class="q-text">{{ currentQuestion.text }}</h2>

        <div class="options">
          <div v-for="opt in currentQuestion.options" :key="opt.key"
            class="option-card"
            :class="{ selected: selectedAnswer === opt.key }"
            :style="selectedAnswer === opt.key ? { borderColor: accentColor, background: accentColor + '14' } : {}"
            @click="selectOption(opt.key)"
          >
            <div class="opt-key" :style="selectedAnswer === opt.key ? { background: accentColor, color: '#fff' } : {}">
              {{ opt.key }}
            </div>
            <div class="opt-text">{{ opt.text }}</div>
            <div v-if="selectedAnswer === opt.key" class="opt-check" :style="{ color: accentColor }">✓</div>
          </div>
        </div>
      </div>

      <div class="btn-row">
        <n-button ghost round size="large" :disabled="currentQIndex === 0"
          :style="{ borderColor: 'rgba(255,255,255,0.15)', color: currentQIndex === 0 ? 'rgba(255,255,255,0.2)' : accentColor }"
          @click="prevQuestion" class="half-btn">
          上一题
        </n-button>
        <n-button type="primary" size="large" :disabled="!selectedAnswer"
          :style="selectedAnswer ? { background: `linear-gradient(135deg, ${accentColor}, ${accentColor2})`, borderColor: 'transparent' } : {}"
          class="half-btn" round @click="nextQuestion">
          {{ isLastQuestion ? '提交本组' : '下一题' }}
        </n-button>
      </div>
    </template>

    <div v-if="submitting" class="loading-overlay">
      <n-spin size="large" />
      <p style="margin-top: 16px; color: rgba(255,255,255,0.6);">分析中...</p>
    </div>
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
const currentStepIndex = ref(1)
const loading = ref(true)
const submitting = ref(false)
const errorMsg = ref('')
const dynamicBg = ref('')

const stageColors = [
  { a: '#4facfe', b: '#2563eb', glow: 'radial-gradient(ellipse at 30% 20%, rgba(79,172,254,0.15) 0%, transparent 60%)', page: 'linear-gradient(135deg, #0a1628 0%, #0f1f3a 50%, #0a1628 100%)' },
  { a: '#2dd4bf', b: '#0d9488', glow: 'radial-gradient(ellipse at 50% 20%, rgba(45,212,191,0.12) 0%, transparent 60%)', page: 'linear-gradient(135deg, #0a1a1a 0%, #0f2d2a 50%, #0a1a1a 100%)' },
  { a: '#a78bfa', b: '#7c3aed', glow: 'radial-gradient(ellipse at 40% 20%, rgba(167,139,250,0.12) 0%, transparent 60%)', page: 'linear-gradient(135deg, #140a28 0%, #1f153a 50%, #140a28 100%)' },
  { a: '#f472b6', b: '#ec4899', glow: 'radial-gradient(ellipse at 60% 20%, rgba(244,114,182,0.12) 0%, transparent 60%)', page: 'linear-gradient(135deg, #280a1a 0%, #3a1528 50%, #280a1a 100%)' },
]

const stageIndex = computed(() => Math.max(0, (poolInfo.value?.stage || 1) - 1))
const accentColor = computed(() => stageColors[stageIndex.value]?.a || '#4facfe')
const accentColor2 = computed(() => stageColors[stageIndex.value]?.b || '#2563eb')
const pageBg = computed(() => {
  if (dynamicBg.value) return dynamicBg.value
  return stageColors[stageIndex.value]?.page || 'linear-gradient(135deg, #0f0c29, #302b63)'
})
const bgGlow = computed(() => stageColors[stageIndex.value]?.glow || '')

const currentQuestion = computed(() => currentQuestions.value[currentQIndex.value] || {})
const answeredCount = computed(() => answers.value.filter(a => a != null).length)
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
    currentStepIndex.value = d.stage
  } catch { errorMsg.value = '⚠️ 加载失败' }
  loading.value = false
}

function selectOption(k) { selectedAnswer.value = k }

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

function prevQuestion() {
  if (currentQIndex.value <= 0) return
  answers.value[currentQIndex.value] = selectedAnswer.value
  currentQIndex.value--
  selectedAnswer.value = answers.value[currentQIndex.value] || null
}

async function submitCurrentPool() {
  submitting.value = true
  try {
    const r = await submitPool(poolId.value, answers.value)
    if (r.data.gradient) dynamicBg.value = r.data.gradient
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
  max-width: 520px; margin: 0 auto; padding: 30px 20px;
  min-height: 100vh; display: flex; flex-direction: column; position: relative;
  transition: background 0.6s ease;
}
.bg-layer {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  pointer-events: none; transition: background 0.6s ease; z-index: 0;
}
.glow-layer {
  position: fixed; top: 0; left: 0; right: 0; height: 60vh;
  pointer-events: none; transition: all 0.6s ease; z-index: 0;
}

.stage-header { text-align: center; margin-bottom: 20px; position: relative; z-index: 1; }
.pool-name { font-size: 20px; font-weight: 700; margin-top: 10px; margin-bottom: 2px; }
.pool-desc { font-size: 13px; color: rgba(255,255,255,0.6); margin-bottom: 6px; }
.q-ref { font-size: 11px; color: rgba(255,255,255,0.18); font-family: monospace; margin-bottom: 12px; letter-spacing: 1px; }
.steps-bar { max-width: 320px; margin: 0 auto; }

.loading-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  min-height: 300px; gap: 16px; position: relative; z-index: 1;
  color: rgba(255,255,255,0.6);
}

.q-area { flex: 1; position: relative; z-index: 1; display: flex; flex-direction: column; justify-content: center; }
.q-progress-text { text-align: right; font-size: 12px; color: rgba(255,255,255,0.5); margin-bottom: 4px; }
.q-progress { margin-bottom: 20px; }
.q-text {
  font-size: 19px; line-height: 1.6; margin-bottom: 22px;
  text-align: center; font-weight: 500;
}

.options { display: flex; flex-direction: column; gap: 8px; }
.option-card {
  display: flex; align-items: center; gap: 12px; padding: 13px 16px;
  background: rgba(255,255,255,0.03); border: 1.5px solid rgba(255,255,255,0.07);
  border-radius: 12px; cursor: pointer; transition: all 0.15s; position: relative;
}
.option-card:hover { background: rgba(255,255,255,0.07); border-color: rgba(255,255,255,0.15); }
.option-card.selected { border-color: var(--accent); }
.opt-key {
  width: 28px; height: 28px; display: flex; align-items: center; justify-content: center;
  background: rgba(255,255,255,0.06); border-radius: 50%; font-weight: 700; font-size: 12px;
  flex-shrink: 0; transition: all 0.15s;
}
.opt-text { font-size: 14px; line-height: 1.4; flex: 1; }
.opt-check { font-size: 16px; font-weight: bold; position: absolute; right: 14px; }

.loading-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15,12,41,0.9); display: flex; flex-direction: column;
  align-items: center; justify-content: center; z-index: 100;
}

/* 按钮行 */
.btn-row {
  display: flex; gap: 10px; position: relative; z-index: 1; margin-top: 4px;
}
.half-btn {
  flex: 1;
}
</style>