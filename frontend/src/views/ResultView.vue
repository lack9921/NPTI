<!-- 结果页 —— 人格 + 五维雷达图 -->
<template>
  <div class="result-page" v-if="result" :style="{ '--accent': colors.base, '--accent2': colors.dark, background: result.gradient || colors.bg }">
    <div class="bg-glow" :style="{ background: `radial-gradient(ellipse at 50% 15%, ${colors.glow} 0%, transparent 60%)` }"></div>

    <div class="result-card">
      <n-gradient-text :size="68" type="info" class="type-badge">{{ result.type }}</n-gradient-text>
      <h1 class="type-title" :style="{ color: colors.base }">{{ result.title }}</h1>
      <p class="type-desc">{{ result.description }}</p>

      <n-divider style="margin: 24px auto; max-width: 160px;" />

      <div class="radar-section">
        <h3 style="font-size: 15px; color: rgba(255,255,255,0.6); margin-bottom: 16px; font-weight: 500;">隐性心理维度</h3>
        <RadarChart :radarData="result.radar_data" height="320px" />
      </div>

      <n-divider style="margin: 24px auto; max-width: 160px;" />

      <div class="report-section" v-if="result.report">
        <h3 style="font-size: 15px; color: rgba(255,255,255,0.6); margin-bottom: 12px; font-weight: 500;">深度分析</h3>
        <div class="report-text">{{ result.report }}</div>
      </div>

      <div style="text-align: center; margin-top: 24px;">
        <n-button ghost round size="large" @click="goHome"
          :style="{ borderColor: colors.base + '55', color: colors.base }">
          再测一次
        </n-button>
      </div>
    </div>
  </div>

  <div v-else class="loading-state"><n-spin size="medium" /></div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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

const typeColors = {
  IPAD: { base: '#4facfe', dark: '#2563eb', glow: 'rgba(79,172,254,0.1)' },
  IPAF: { base: '#38bdf8', dark: '#0284c7', glow: 'rgba(56,189,248,0.1)' },
  IPCD: { base: '#a78bfa', dark: '#7c3aed', glow: 'rgba(167,139,250,0.1)' },
  IPCF: { base: '#c084fc', dark: '#9333ea', glow: 'rgba(192,132,252,0.1)' },
  ISAD: { base: '#60a5fa', dark: '#3b82f6', glow: 'rgba(96,165,250,0.1)' },
  ISAF: { base: '#34d399', dark: '#059669', glow: 'rgba(52,211,153,0.1)' },
  ISCD: { base: '#f472b6', dark: '#db2777', glow: 'rgba(244,114,182,0.1)' },
  ISCF: { base: '#fb923c', dark: '#ea580c', glow: 'rgba(251,146,60,0.1)' },
  RPAD: { base: '#818cf8', dark: '#6366f1', glow: 'rgba(129,140,248,0.1)' },
  RPAF: { base: '#2dd4bf', dark: '#0d9488', glow: 'rgba(45,212,191,0.1)' },
  RPCD: { base: '#e879f9', dark: '#c026d3', glow: 'rgba(232,121,249,0.1)' },
  RPCF: { base: '#fbbf24', dark: '#d97706', glow: 'rgba(251,191,36,0.1)' },
  RSAD: { base: '#6b7280', dark: '#4b5563', glow: 'rgba(107,114,128,0.1)' },
  RSAF: { base: '#9ca3af', dark: '#6b7280', glow: 'rgba(156,163,175,0.1)' },
  RSCD: { base: '#94a3b8', dark: '#64748b', glow: 'rgba(148,163,184,0.1)' },
  RSCF: { base: '#cbd5e1', dark: '#94a3b8', glow: 'rgba(203,213,225,0.1)' },
}

const colors = computed(() => typeColors[result.value?.type] || { base: '#667eea', dark: '#764ba2', glow: 'rgba(102,126,234,0.1)', bg: 'linear-gradient(135deg, #0f0c29, #302b63)' })

function goHome() { router.push('/') }
</script>

<style scoped>
.result-page {
  min-height: 100vh; padding: 40px 20px;
  display: flex; align-items: flex-start; justify-content: center; position: relative;
}
.bg-glow {
  position: fixed; top: 0; left: 0; right: 0; height: 60vh;
  pointer-events: none; transition: all 0.8s ease; z-index: 0;
}
.result-card { max-width: 500px; width: 100%; text-align: center; position: relative; z-index: 1; }
.type-badge { letter-spacing: 10px; line-height: 1; margin-bottom: 10px; display: inline-block; }
.type-title { font-size: 24px; margin-bottom: 10px; }
.type-desc { color: rgba(255,255,255,0.55); line-height: 1.7; font-size: 14px; }
.radar-section { margin-top: 8px; }
.report-section { text-align: left; }
.report-text {
  font-size: 14px; line-height: 1.9; color: rgba(255,255,255,0.7);
  white-space: pre-line;
}

.loading-state {
  display: flex; align-items: center; justify-content: center; min-height: 100vh;
}
</style>
