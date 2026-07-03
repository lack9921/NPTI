<template>
  <div class="test-page">
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
    </div>
    <div class="progress-text">第 {{ currentIndex + 1 }} / {{ questions.length }} 题</div>

    <div class="question-card" v-if="questions.length > 0">
      <h2 class="q-text">{{ questions[currentIndex].text }}</h2>
      <div class="options">
        <div
          v-for="opt in questions[currentIndex].options"
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

    <div class="nav-buttons">
      <button
        class="nav-btn"
        :disabled="currentIndex === 0"
        @click="prevQuestion"
      >上一题</button>
      <button
        class="nav-btn primary"
        :disabled="!selectedAnswer"
        @click="nextQuestion"
      >
        {{ currentIndex === questions.length - 1 ? '提交答案' : '下一题' }}
      </button>
    </div>

    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>正在分析你的答案...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getQuestions, submitAnswers } from '../api/request.js'

const router = useRouter()
const questions = ref([])
const currentIndex = ref(0)
const answers = ref([])
const selectedAnswer = ref(null)
const loading = ref(false)

const progressPercent = computed(() => {
  if (questions.value.length === 0) return 0
  return ((currentIndex.value + 1) / questions.value.length) * 100
})

onMounted(async () => {
  try {
    const res = await getQuestions()
    questions.value = res.data.data
  } catch {
    // 如果后端没启动，用假数据兜底
    questions.value = getMockQuestions()
  }
})

function selectOption(key) {
  selectedAnswer.value = key
}

function nextQuestion() {
  if (!selectedAnswer.value) return
  answers.value[currentIndex.value] = selectedAnswer.value

  if (currentIndex.value === questions.value.length - 1) {
    submitTest()
    return
  }

  currentIndex.value++
  selectedAnswer.value = answers.value[currentIndex.value] || null
}

function prevQuestion() {
  if (currentIndex.value > 0) {
    answers.value[currentIndex.value] = selectedAnswer.value
    currentIndex.value--
    selectedAnswer.value = answers.value[currentIndex.value] || null
  }
}

async function submitTest() {
  loading.value = true
  try {
    const res = await submitAnswers(answers.value)
    router.push({ name: 'Result', query: { data: JSON.stringify(res.data.data) } })
  } catch {
    // 后端不通时用假数据演示
    const mockResult = {
      nptiType: "INTJ",
      title: "建筑师型人格",
      description: "富有想象力、战略性、果断。你是一个天生的规划者，总能从全局视角看到问题的本质，并制定出最优方案。",
      dimensions: [
        { name: "精力来源", abbr: "I", score: 8, opposite: "E" },
        { name: "认知方式", abbr: "N", score: 9, opposite: "S" },
        { name: "决策方式", abbr: "T", score: 7, opposite: "F" },
        { name: "生活态度", abbr: "J", score: 8, opposite: "P" }
      ],
      radarData: [
        { name: "I/E", value: 56 },
        { name: "N/S", value: 67 },
        { name: "T/F", value: 44 },
        { name: "J/P", value: 56 }
      ]
    }
    router.push({ name: 'Result', query: { data: JSON.stringify(mockResult) } })
  }
  loading.value = false
}

function getMockQuestions() {
  return [
    { id: 1, text: "周末你更倾向于？", options: [
      { key: "A", text: "约朋友出去玩" }, { key: "B", text: "在家打游戏或看书" },
      { key: "C", text: "参加线下活动聚会" }, { key: "D", text: "一个人安静待着" }
    ]},
    { id: 2, text: "在团队讨论中，你通常？", options: [
      { key: "A", text: "积极发言，带动气氛" }, { key: "B", text: "认真听，偶尔插话" },
      { key: "C", text: "主导话题走向" }, { key: "D", text: "默默记笔记，心里有数" }
    ]},
    { id: 3, text: "你交朋友的方式是？", options: [
      { key: "A", text: "主动认识，扩宽圈子" }, { key: "B", text: "通过共同朋友认识" },
      { key: "C", text: "在各种场合都能自来熟" }, { key: "D", text: "随缘，不主动社交" }
    ]},
    { id: 4, text: "你更喜欢哪种类型的问题？", options: [
      { key: "A", text: "有明确答案的具体问题" }, { key: "B", text: "需要想象力的开放问题" },
      { key: "C", text: "跟实际生活相关的实用问题" }, { key: "D", text: "充满可能性的抽象问题" }
    ]},
    { id: 5, text: "看说明书时，你通常会？", options: [
      { key: "A", text: "一步一步照着做" }, { key: "B", text: "扫一眼大概，自己摸索" },
      { key: "C", text: "只关注关键步骤" }, { key: "D", text: "凭直觉操作，出问题再看" }
    ]},
    { id: 6, text: "你更容易记住？", options: [
      { key: "A", text: "具体发生过的事情细节" }, { key: "B", text: "当时的感受和整体氛围" },
      { key: "C", text: "事实和数据" }, { key: "D", text: "对未来的联想和可能" }
    ]},
    { id: 7, text: "朋友向你倾诉烦恼，你第一反应是？", options: [
      { key: "A", text: "帮ta分析问题出在哪" }, { key: "B", text: "理解ta的感受，表示支持" },
      { key: "C", text: "直接给解决方案" }, { key: "D", text: "陪着ta，说什么不重要" }
    ]},
    { id: 8, text: "做重要决定时，你更依赖？", options: [
      { key: "A", text: "逻辑分析和事实依据" }, { key: "B", text: "内心的价值观和感受" },
      { key: "C", text: "效率和收益最大化" }, { key: "D", text: "这件事对人际关系的影响" }
    ]},
    { id: 9, text: "别人对你提出批评，你通常？", options: [
      { key: "A", text: "先看ta说得有没有道理" }, { key: "B", text: "有点受伤，但会反思" },
      { key: "C", text: "如果没道理就直接忽略" }, { key: "D", text: "在意对方的感受多于对错" }
    ]},
    { id: 10, text: "你的书桌/工作区通常是？", options: [
      { key: "A", text: "整整齐齐，每样东西有固定位置" }, { key: "B", text: "有自己的一套乱序但找得到" },
      { key: "C", text: "定期收拾，但日常会乱" }, { key: "D", text: "随心所欲，懒得整理" }
    ]},
    { id: 11, text: "你更喜欢哪种生活方式？", options: [
      { key: "A", text: "提前制定好计划按部就班" }, { key: "B", text: "有大方向但细节随缘" },
      { key: "C", text: "排好优先级按重要程度来" }, { key: "D", text: "想到什么做什么，随性" }
    ]},
    { id: 12, text: "面对未预期的变化，你的态度是？", options: [
      { key: "A", text: "不太喜欢，希望按原计划走" }, { key: "B", text: "可以接受，随机应变" },
      { key: "C", text: "有点烦躁但能调整" }, { key: "D", text: "拥抱变化，觉得很有趣" }
    ]}
  ]
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
}
.progress-bar {
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
  text-align: center;
  color: rgba(255,255,255,0.5);
  font-size: 14px;
  margin-bottom: 40px;
}
.question-card {
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
  padding: 16px 20px;
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
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
  flex-shrink: 0;
}
.option.selected .option-key {
  background: #667eea;
}
.option-text {
  font-size: 16px;
}
.nav-buttons {
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
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255,255,255,0.1);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
