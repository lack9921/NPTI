<!--
  ResultView.vue —— NPFJ 测试结果页
  人格类型 + 五维雷达图 + 动态配色
-->
<template>
  <div class="result-page" :style="result ? { '--accent': colors.base, '--accent2': colors.dark, '--glow': colors.glow } : {}">
    <div class="bg-glow" :style="{ background: `radial-gradient(ellipse at 50% 20%, ${colors.glow} 0%, transparent 60%)` }" v-if="result"></div>

    <div class="result-card" v-if="result">
      <div class="type-badge">{{ result.type }}</div>
      <h1 class="type-title" :style="{ color: colors.base }">{{ result.title }}</h1>
      <p class="type-desc">{{ result.description }}</p>

      <div class="divider" :style="{ background: `linear-gradient(90deg, transparent, ${colors.base}44, transparent)` }"></div>

      <div class="radar-section">
        <h3>隐性心理维度</h3>
        <RadarChart :radarData="result.radar_data" height="340px" />
      </div>

      <button class="retry-btn" @click="goHome"
        :style="{ borderColor: colors.base + '44', color: colors.base }"
        @mouseenter="$event.target.style.borderColor = colors.base"
        @mouseleave="$event.target.style.borderColor = colors.base + '44'">
        再测一次
      </button>
    </div>

    <div v-else class="loading-state"><p>加载中...</p></div>
  </div>
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

// 人格类型配色（16 种人格 × 16 套颜色）
const typeColors = {
  IPAD: { base: '#4facfe', dark: '#2563eb', glow: 'rgba(79,172,254,0.12)' },
  IPAF: { base: '#38bdf8', dark: '#0284c7', glow: 'rgba(56,189,248,0.12)' },
  IPCD: { base: '#a78bfa', dark: '#7c3aed', glow: 'rgba(167,139,250,0.12)' },
  IPCF: { base: '#c084fc', dark: '#9333ea', glow: 'rgba(192,132,252,0.12)' },
  ISAD: { base: '#60a5fa', dark: '#3b82f6', glow: 'rgba(96,165,250,0.12)' },
  ISAF: { base: '#34d399', dark: '#059669', glow: 'rgba(52,211,153,0.12)' },
  ISCD: { base: '#f472b6', dark: '#db2777', glow: 'rgba(244,114,182,0.12)' },
  ISCF: { base: '#fb923c', dark: '#ea580c', glow: 'rgba(251,146,60,0.12)' },
  RPAD: { base: '#818cf8', dark: '#6366f1', glow: 'rgba(129,140,248,0.12)' },
  RPAF: { base: '#2dd4bf', dark: '#0d9488', glow: 'rgba(45,212,191,0.12)' },
  RPCD: { base: '#e879f9', dark: '#c026d3', glow: 'rgba(232,121,249,0.12)' },
  RPCF: { base: '#fbbf24', dark: '#d97706', glow: 'rgba(251,191,36,0.12)' },
  RSAD: { base: '#6b7280', dark: '#4b5563', glow: 'rgba(107,114,128,0.12)' },
  RSAF: { base: '#9ca3af', dark: '#6b7280', glow: 'rgba(156,163,175,0.12)' },
  RSCD: { base: '#94a3b8', dark: '#64748b', glow: 'rgba(148,163,184,0.12)' },
  RSCF: { base: '#cbd5e1', dark: '#94a3b8', glow: 'rgba(203,213,225,0.12)' },
}

const colors = computed(() => typeColors[result.value?.type] || { base: '#667eea', dark: '#764ba2', glow: 'rgba(102,126,234,0.12)' })

function goHome() { router.push('/') }
</script>

<style scoped>
.result-page {
  min-height: 100vh; padding: 40px 20px;
  display: flex; align-items: flex-start; justify-content: center;
  position: relative;
}
.bg-glow {
  position: fixed; top: 0; left: 0; right: 0; height: 60vh;
  pointer-events: none; transition: all 0.8s ease; z-index: 0;
}
.result-card { max-width: 520px; width: 100%; text-align: center; position: relative; z-index: 1; }

.type-badge {
  font-size: 72px; font-weight: 900; letter-spacing: 12px;
  background: linear-gradient(135deg, var(--accent, #667eea), var(--accent2, #764ba2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; margin-bottom: 12px; line-height: 1;
}
.type-title { font-size: 26px; margin-bottom: 12px; }
.type-desc { color: rgba(255,255,255,0.6); line-height: 1.7; font-size: 14px; margin-bottom: 28px; }

.divider { height: 1px; margin: 0 auto 28px; max-width: 200px; }

.radar-section h3 { font-size: 16px; margin-bottom: 16px; color: rgba(255,255,255,0.8); }

.retry-btn {
  padding: 12px 44px; font-size: 15px; background: transparent;
  border-radius: 50px; cursor: pointer; transition: all 0.2s; margin-top: 10px;
}
.retry-btn:hover { background: rgba(255,255,255,0.05); transform: translateY(-1px); }

.loading-state { display: flex; align-items: center; justify-content: center; min-height: 100vh; }
</style>
