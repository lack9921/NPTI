<!--
  TestView.vue —— 答题页（核心交互页面）

  流程：
  1. 页面加载时从后端获取题目列表（getQuestions）
  2. 显示当前题目和四个选项，点击选项选中
  3. 点击"下一题"保存答案并切换到下一题
  4. 全部 12 题答完后，点击"提交答案"调用后端算分接口
  5. 拿到结果后跳转到结果页（/result）

  如果后端没启动，自动使用内置的假数据（mock），不会卡住。
-->
<template>
  <div class="test-page">
    <!-- 顶部进度条：显示答题进度 -->
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
    </div>
    <div class="progress-text">第 {{ currentIndex + 1 }} / {{ questions.length }} 题</div>

    <!-- 题目卡片：显示当前题目和四个选项 -->
    <div class="question-card" v-if="questions.length > 0">
      <h2 class="q-text">{{ questions[currentIndex].text }}</h2>
      <div class="options">
        <!--
          v-for 循环渲染四个选项
          :class 动态绑定样式：选中的选项高亮
          @click 点击时记录选中的答案
        -->
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

    <!-- 底部按钮：上一题 / 下一题（最后一题显示"提交答案"） -->
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

    <!-- 提交后的加载动画 -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>正在分析你的答案...</p>
    </div>
  </div>
</template>

<script setup>
/**
 * Vue 3 组合式 API
 * ref：创建响应式数据（值改变时页面自动更新）
 * computed：根据其他数据计算出的值
 * onMounted：组件挂载后自动执行
 */
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getQuestions, submitAnswers } from '../api/request.js'

const router = useRouter()

// ======== 响应式数据（页面会根据这些值的变化自动刷新） ========

const questions = ref([])      // 所有题目的数据
const currentIndex = ref(0)    // 当前第几题（从 0 开始）
const answers = ref([])        // 存储所有已选的答案
const selectedAnswer = ref(null)  // 当前题目选中的选项
const loading = ref(false)     // 是否正在提交

// 计算属性：当前答题进度百分比
const progressPercent = computed(() => {
  if (questions.value.length === 0) return 0
  return ((currentIndex.value + 1) / questions.value.length) * 100
})

// ======== 生命周期：页面加载时自动执行 ========

onMounted(async () => {
  try {
    // 尝试从后端获取题目
    const res = await getQuestions()
    questions.value = res.data.data
  } catch {
    // 如果后端没启动（报错），用内置假数据
    // 这样在没有后端的情况下也能演示
    questions.value = getMockQuestions()
  }
})

// ======== 交互方法 ========

/** 点击选项时调用，记录选中的答案 */
function selectOption(key) {
  selectedAnswer.value = key
}

/** 点击"下一题"或"提交"时调用 */
function nextQuestion() {
  if (!selectedAnswer.value) return  // 没选答案就忽略

  // 保存当前题的答案
  answers.value[currentIndex.value] = selectedAnswer.value

  // 如果是最后一题，提交所有答案
  if (currentIndex.value === questions.value.length - 1) {
    submitTest()
    return
  }

  // 否则切换到下一题
  currentIndex.value++
  // 如果之前已经答过这题，恢复之前选的答案
  selectedAnswer.value = answers.value[currentIndex.value] || null
}

/** 回到上一题，保留已选的答案 */
function prevQuestion() {
  if (currentIndex.value > 0) {
    answers.value[currentIndex.value] = selectedAnswer.value
    currentIndex.value--
    selectedAnswer.value = answers.value[currentIndex.value] || null
  }
}

/** 提交所有答案到后端，获取测试结果 */
async function submitTest() {
  loading.value = true
  try {
    // 调用后端 API 计算性格类型
    const res = await submitAnswers(answers.value)
    // 把结果数据通过 URL 参数传给结果页
    router.push({ name: 'Result', query: { data: JSON.stringify(res.data.data) } })
  } catch {
    // 后端不通时，用假数据演示结果
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
        { name: "F/T", value: 44 },
        { name: "P/J", value: 56 }
      ]
    }
    router.push({ name: 'Result', query: { data: JSON.stringify(mockResult) } })
  }
  loading.value = false
}

// ======== 假数据（当后端没启动时使用） ========

/**
 * 内置 12 道题的假数据
 * 结构和后端返回的格式完全一致
 * 这样即使后端没启动，前端也能正常演示
 */
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
/* 整个页面布局 */
.test-page {
  max-width: 640px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部进度条 */
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

/* 题目卡片 */
.question-card {
  flex: 1;
}
.q-text {
  font-size: 22px;
  line-height: 1.5;
  margin-bottom: 30px;
  text-align: center;
}

/* 选项列表 */
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
/* 选中的选项高亮 */
.option.selected {
  background: rgba(102,126,234,0.2);
  border-color: #667eea;
}
/* 选项旁边的字母标识（A/B/C/D） */
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

/* 底部导航按钮 */
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

/* 提交后的全屏加载动画 */
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
