<!--
  TestView.vue —— NPFJ 动态路由答题页

  新的答题流程：
  1. 进入页面 → 创建会话 → 加载 Stage 1 题池（5 题）
  2. 用户作答 5 题 → 点击提交 → 后端路由到下一题池
  3. 加载下一个题池 → 继续作答
  4. 重复直到 is_final = true → 跳转结果页

  每个题池固定 5 题，选项 A/B，不暴露任何权重信息给前端。
-->
<template>
  <div class="test-page">
    <!-- 顶部：路径进度和阶段信息 -->
    <div class="stage-header">
      <div class="stage-badge" v-if="poolInfo">阶段 {{ poolInfo.stage }} / 4</div>
      <div class="pool-name" v-if="poolInfo">{{ poolInfo.name }}</div>
      <div class="pool-desc" v-if="poolInfo">{{ poolInfo.description }}</div>
      <!-- 路径指示器 -->
      <div class="path-indicator">
        <span
          v-for="(step, i) in pathSteps"
          :key="i"
          class="path-dot"
          :class="{ active: step.done, current: step.active }"
        >
          {{ step.done ? step.letter : i + 1 }}
        </span>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 题目区域 -->
    <template v-if="!loading && currentQuestions.length > 0">
      <!-- 进度：题内进度 -->
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: ((answeredCount) / 5 * 100) + '%' }"></div>
      </div>
      <div class="progress-text">第 {{ answeredCount + 1 }} / 5 题</div>

      <!-- 当前题目 -->
      <div class="question-card">
        <h2 class="q-text">{{ currentQuestion.text }}</h2>
        <div class="options">
          <div
            v-for="opt in currentQuestion.options"
            :key="opt.key"
            class="option"
            :class="{ selected: selectedAnswer === opt.key }"
            @click="selectOption(opt.key)"
          >
            <span class="option-key">{{ opt.key }}</span>
            <span class="option-text">{{ opt.text }}</span>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="nav-buttons">
        <button class="nav-btn primary" :disabled="!selectedAnswer" @click="nextQuestion">
          {{ isLastQuestion ? '提交本组' : '下一题' }}
        </button>
      </div>
    </template>

    <!-- 提交后的加载动画 -->
    <div v-if="submitting" class="loading-overlay">
      <div class="spinner"></div>
      <p>正在分析你的答案...</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="errorMsg" class="error-toast">{{ errorMsg }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createSession, getPool, submitPool, getResult } from '../api/request.js'

const router = useRouter()

// ======== 状态 ========
const sessionId = ref(null)
const poolId = ref(1)
const poolInfo = ref(null)
const currentQuestions = ref([])
const currentQIndex = ref(0)
const answers = ref([])      // 当前题池的 5 个答案
const selectedAnswer = ref(null)
const pathSteps = ref([])    // [{ direction, letter, done, active }]
const loading = ref(true)
const submitting = ref(false)
const errorMsg = ref('')

// ======== 计算属性 ========
const currentQuestion = computed(() => {
  return currentQuestions.value[currentQIndex.value] || {}
})
const answeredCount = computed(() => {
  return answers.value.filter(a => a !== undefined && a !== null).length
})
const isLastQuestion = computed(() => {
  return currentQIndex.value === currentQuestions.value.length - 1
})

// ======== 生命周期 ========
onMounted(async () => {
  try {
    // 1. 创建会话
    const sessionRes = await createSession()
    sessionId.value = sessionRes.data.session_id

    // 2. 加载第一个题池
    const firstPoolId = sessionRes.data.first_pool
    await loadPool(firstPoolId)
  } catch {
    errorMsg.value = '⚠️ 后端未连接，请确保后端已启动'
    loading.value = false
  }
})

// ======== 方法 ========

/** 加载指定题池 */
async function loadPool(id) {
  loading.value = true
  try {
    const res = await getPool(id)
    const data = res.data
    poolId.value = data.id
    poolInfo.value = { stage: data.stage, name: data.name, description: data.description }
    currentQuestions.value = data.questions
    currentQIndex.value = 0
    answers.value = []
    selectedAnswer.value = null

    // 更新路径指示器
    updatePathSteps(data.stage)
  } catch {
    errorMsg.value = '⚠️ 加载题库失败'
  }
  loading.value = false
}

/** 更新路径指示器 */
function updatePathSteps(stage) {
  const total = 4  // 4 个维度，各 1 个题池
  const steps = []
  const stageNames = ['能量', '参与', '认知', '表达']
  for (let i = 0; i < total; i++) {
    const letter = pathSteps.value[i]?.letter
    steps.push({
      label: stageNames[i] || `阶段${i}`,
      done: i < stage,
      active: i === stage,
      letter: letter || null,
    })
  }
  pathSteps.value = steps
}

/** 选中选项 */
function selectOption(key) {
  selectedAnswer.value = key
}

/** 下一题或提交本组 */
async function nextQuestion() {
  if (!selectedAnswer.value) return

  answers.value[currentQIndex.value] = selectedAnswer.value

  if (!isLastQuestion.value) {
    // 同一题池内翻到下一题
    currentQIndex.value++
    selectedAnswer.value = null
    return
  }

  // 最后一道题 → 提交整个题池
  await submitCurrentPool()
}

/** 提交当前题池的 5 个答案 */
async function submitCurrentPool() {
  submitting.value = true
  try {
    const res = await submitPool(poolId.value, answers.value)
    const data = res.data

    if (data.is_final) {
      // 所有阶段完成 → 获取最终结果
      const resultRes = await getResult()
      router.push({ name: 'Result', query: { data: JSON.stringify(resultRes.data) } })
    } else if (data.next_pool !== null && data.next_pool !== undefined) {
      // 路由到下一题池
      await loadPool(data.next_pool)
    }
  } catch {
    errorMsg.value = '⚠️ 提交失败，请重试'
    setTimeout(() => { errorMsg.value = '' }, 3000)
  }
  submitting.value = false
}
</script>

<style scoped>
.test-page {
  max-width: 640px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 阶段头部 */
.stage-header {
  text-align: center;
  margin-bottom: 30px;
  width: 100%;
}
.stage-badge {
  display: inline-block;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  padding: 4px 16px;
  border-radius: 12px;
  font-size: 12px;
  letter-spacing: 2px;
  margin-bottom: 12px;
}
.pool-name {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 6px;
}
.pool-desc {
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  margin-bottom: 16px;
}

/* 路径指示器 */
.path-indicator {
  display: flex;
  justify-content: center;
  gap: 8px;
}
.path-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  border: 2px solid rgba(255,255,255,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: all 0.3s;
}
.path-dot.active {
  background: rgba(102,126,234,0.3);
  border-color: #667eea;
}
.path-dot.current {
  background: rgba(102,126,234,0.5);
  border-color: #764ba2;
  box-shadow: 0 0 12px rgba(102,126,234,0.4);
}

/* 进度条 */
.progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(255,255,255,0.1);
  border-radius: 3px;
  margin-bottom: 8px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.3s ease;
}
.progress-text {
  width: 100%;
  text-align: center;
  color: rgba(255,255,255,0.5);
  font-size: 14px;
  margin-bottom: 30px;
}

/* 题目 */
.question-card {
  width: 100%;
  flex: 1;
}
.q-text {
  font-size: 22px;
  line-height: 1.5;
  margin-bottom: 30px;
  text-align: center;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.option {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  background: rgba(255,255,255,0.05);
  border: 2px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}
.option:hover {
  background: rgba(255,255,255,0.1);
  border-color: rgba(255,255,255,0.2);
}
.option.selected {
  background: rgba(102,126,234,0.2);
  border-color: #667eea;
}
.option-key {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  font-weight: bold;
  font-size: 16px;
  flex-shrink: 0;
}
.option.selected .option-key {
  background: #667eea;
}
.option-text {
  font-size: 16px;
}

/* 按钮 */
.nav-buttons {
  width: 100%;
  display: flex;
  gap: 12px;
  margin-top: 30px;
}
.nav-btn {
  flex: 1;
  padding: 14px;
  border: 2px solid rgba(255,255,255,0.2);
  background: transparent;
  color: #fff;
  border-radius: 12px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}
.nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
.nav-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
}
.nav-btn.primary:disabled {
  background: rgba(255,255,255,0.1);
}

/* 加载动画 */
.loading-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15,12,41,0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  z-index: 100;
}
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
  color: rgba(255,255,255,0.6);
}
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255,255,255,0.1);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* 错误提示 */
.error-toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 107, 107, 0.9);
  color: #fff;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  z-index: 200;
  box-shadow: 0 4px 20px rgba(255, 107, 107, 0.3);
}
</style>
