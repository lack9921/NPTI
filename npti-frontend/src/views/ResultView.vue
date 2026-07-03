<!--
  ResultView.vue —— 测试结果页

  显示用户的 NPTI 人格类型，包括：
  1. 大号四位字母（如 INTJ）
  2. 人格标题和详细描述
  3. ECharts 雷达图（四个维度的雷达图可视化）
  4. 每个维度的具体分数条
  5. "再测一次"按钮回到首页

  数据通过 URL 参数 data 传递（JSON 字符串格式）
-->
<template>
  <div class="result-page">
    <div class="result-card" v-if="result">
      <!-- 大号四位字母：渐变颜色 -->
      <div class="type-badge">{{ result.nptiType }}</div>

      <!-- 人格标题和描述 -->
      <h1 class="type-title">{{ result.title }}</h1>
      <p class="type-desc">{{ result.description }}</p>

      <!-- 雷达图区域：四个维度的可视化 -->
      <div class="radar-section">
        <h3>人格维度分析</h3>
        <RadarChart :radarData="result.radarData" height="350px" />
      </div>

      <!-- 详细维度评分条 -->
      <div class="dimensions-section">
        <h3>详细维度评分</h3>
        <div class="dimension-item" v-for="dim in result.dimensions" :key="dim.name">
          <div class="dim-header">
            <span class="dim-name">{{ dim.name }}</span>
            <!-- 显示当前分数偏向哪一边，如 I / E -->
            <span class="dim-type">{{ dim.abbr }} / {{ dim.opposite }}</span>
          </div>
          <!-- 分数进度条 -->
          <div class="dim-bar-bg">
            <div class="dim-bar-fill" :style="{ width: normalizeScore(dim.score) + '%' }"></div>
          </div>
          <div class="dim-score">{{ dim.score }} 分</div>
        </div>
      </div>

      <!-- 再测一次按钮 -->
      <button class="retry-btn" @click="goHome">再测一次</button>
    </div>

    <!-- 数据还没加载时显示 -->
    <div v-else class="loading-state">
      <p>数据加载中...</p>
    </div>
  </div>
</template>

<script setup>
/**
 * 结果页逻辑
 *
 * 从 URL 参数中读取测试结果数据（由 TestView 传过来）
 * 展示人格类型、描述、雷达图、维度评分
 */
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import RadarChart from '../components/RadarChart.vue'

const route = useRoute()   // 获取当前路由，读取 URL 参数
const router = useRouter() // 用于跳转回首页
const result = ref(null)   // 测试结果数据

// 页面加载时，从 URL 参数中解析结果数据
onMounted(() => {
  try {
    const raw = route.query.data  // URL 中的 data 参数（JSON 字符串）
    if (raw) result.value = JSON.parse(raw)
  } catch {
    // 解析失败就保持 null，显示"数据加载中"
  }
})

/**
 * 把原始分数（3-12）映射到百分比（0-100）
 * 公式：(当前分 - 最低分) / (最高分 - 最低分) * 100
 */
function normalizeScore(score) {
  return Math.max(0, Math.min(100, (score - 3) * 100 / 9))
}

/** 回到首页 */
function goHome() {
  router.push('/')
}
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  padding: 40px 20px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}
.result-card {
  max-width: 560px;
  width: 100%;
  text-align: center;
}

/* 大号四位人格类型字母 */
.type-badge {
  display: inline-block;
  font-size: 64px;
  font-weight: 900;
  letter-spacing: 8px;
  background: linear-gradient(135deg, #667eea, #f093fb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
}
.type-title {
  font-size: 28px;
  margin-bottom: 16px;
}
.type-desc {
  color: rgba(255,255,255,0.7);
  line-height: 1.8;
  font-size: 15px;
  margin-bottom: 40px;
}

/* 雷达图区域 */
.radar-section, .dimensions-section {
  margin-bottom: 40px;
  text-align: left;
}
.radar-section h3, .dimensions-section h3 {
  font-size: 18px;
  margin-bottom: 20px;
  text-align: center;
}

/* 维度评分条 */
.dimension-item {
  margin-bottom: 20px;
}
.dim-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}
.dim-name { color: rgba(255,255,255,0.8); }
.dim-type { color: rgba(255,255,255,0.5); }
.dim-bar-bg {
  height: 8px;
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
  overflow: hidden;
}
.dim-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.8s ease;
}
.dim-score {
  text-align: right;
  font-size: 12px;
  color: rgba(255,255,255,0.4);
  margin-top: 4px;
}

/* 再测一次按钮 */
.retry-btn {
  padding: 14px 48px;
  font-size: 16px;
  border: 2px solid rgba(255,255,255,0.2);
  background: transparent;
  color: #fff;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s;
}
.retry-btn:hover {
  background: rgba(255,255,255,0.1);
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
</style>
