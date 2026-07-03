<!--
  ResultView.vue —— NPFJ 测试结果页

  显示内容：
  1. 4 位人格类型字母 + 标题 + 描述
  2. 路径决策历史
  3. 四维人格分析（阶段得分）
  4. 五维隐性权重雷达图（核心创新点）
-->
<template>
  <div class="result-page">
    <div class="result-card" v-if="result">
      <!-- 人格类型（大号渐变字母） -->
      <div class="type-badge">{{ result.type }}</div>
      <h1 class="type-title">{{ result.title }}</h1>
      <p class="type-desc">{{ result.description }}</p>

      <!-- 路径决策历史 -->
      <div class="path-section" v-if="result.path_letters">
        <h3>决策路径</h3>
        <div class="path-steps">
          <div class="path-step" v-for="(step, i) in result.path_letters" :key="i">
            <div class="step-stage">{{ step.stage }}</div>
            <div class="step-letter">{{ step.letter }}</div>
            <div class="step-direction">{{ step.direction === 'L' ? '← 左' : '右 →' }}</div>
          </div>
        </div>
      </div>

      <!-- 五维雷达图 -->
      <div class="radar-section">
        <h3>隐性心理维度分析 🧠</h3>
        <RadarChart :radarData="result.radar_data" height="380px" />
      </div>

      <!-- 四维人格分析 -->
      <div class="dimensions-section" v-if="result.dimensions">
        <h3>人格维度分布</h3>
        <div class="dimension-item" v-for="dim in result.dimensions" :key="dim.name">
          <div class="dim-header">
            <span class="dim-name">{{ dim.name }}</span>
            <span class="dim-type">{{ dim.abbr }} / {{ dim.opposite }}</span>
          </div>
          <div class="dim-bar-bg">
            <div class="dim-bar-fill" :style="{ width: (dim.score / 12 * 100) + '%' }"></div>
          </div>
          <div class="dim-score">{{ dim.score }} 分</div>
        </div>
      </div>

      <!-- 再测一次 -->
      <button class="retry-btn" @click="goHome">再测一次</button>
    </div>

    <div v-else class="loading-state">
      <p>数据加载中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import RadarChart from '../components/RadarChart.vue'

const route = useRoute()
const router = useRouter()
const result = ref(null)

onMounted(() => {
  try {
    const raw = route.query.data
    if (raw) result.value = JSON.parse(raw)
  } catch {}
})

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
  max-width: 600px;
  width: 100%;
  text-align: center;
}

.type-badge {
  display: inline-block;
  font-size: 64px;
  font-weight: 900;
  letter-spacing: 10px;
  background: linear-gradient(135deg, #667eea, #f093fb, #4facfe);
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

/* 路径历史 */
.path-section {
  margin-bottom: 40px;
  text-align: left;
}
.path-section h3 {
  text-align: center;
  margin-bottom: 16px;
  font-size: 18px;
}
.path-steps {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}
.path-step {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 12px 16px;
  text-align: center;
  min-width: 80px;
}
.step-stage {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  margin-bottom: 4px;
}
.step-letter {
  font-size: 22px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.step-direction {
  font-size: 11px;
  color: rgba(255,255,255,0.5);
  margin-top: 2px;
}

/* 五维雷达图 */
.radar-section {
  margin-bottom: 40px;
}
.radar-section h3 {
  font-size: 18px;
  margin-bottom: 20px;
}

/* 维度评分 */
.dimensions-section {
  margin-bottom: 40px;
  text-align: left;
}
.dimensions-section h3 {
  text-align: center;
  font-size: 18px;
  margin-bottom: 20px;
}
.dimension-item {
  margin-bottom: 16px;
}
.dim-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
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
  margin-top: 2px;
}

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
