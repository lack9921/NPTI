<template>
  <div class="result-page">
    <div class="result-card" v-if="result">
      <div class="type-badge">{{ result.nptiType }}</div>
      <h1 class="type-title">{{ result.title }}</h1>
      <p class="type-desc">{{ result.description }}</p>

      <div class="radar-section">
        <h3>人格维度分析</h3>
        <RadarChart :radarData="result.radarData" height="350px" />
      </div>

      <div class="dimensions-section">
        <h3>详细维度评分</h3>
        <div class="dimension-item" v-for="dim in result.dimensions" :key="dim.name">
          <div class="dim-header">
            <span class="dim-name">{{ dim.name }}</span>
            <span class="dim-type">{{ dim.abbr }} / {{ dim.opposite }}</span>
          </div>
          <div class="dim-bar-bg">
            <div class="dim-bar-fill" :style="{ width: normalizeScore(dim.score) + '%' }"></div>
          </div>
          <div class="dim-score">{{ dim.score }} 分</div>
        </div>
      </div>

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

function normalizeScore(score) {
  return Math.max(0, Math.min(100, (score - 3) * 100 / 9))
}

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
.radar-section, .dimensions-section {
  margin-bottom: 40px;
  text-align: left;
}
.radar-section h3, .dimensions-section h3 {
  font-size: 18px;
  margin-bottom: 20px;
  text-align: center;
}
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
