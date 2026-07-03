<template>
  <div ref="chartRef" :style="{ width, height }"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  radarData: { type: Array, default: () => [] },
  width: { type: String, default: '100%' },
  height: { type: String, default: '400px' }
})

const chartRef = ref(null)
let chartInstance = null

function initChart() {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

function updateChart() {
  if (!chartInstance || props.radarData.length === 0) return

  const indicators = props.radarData.map(item => ({
    name: item.name,
    max: 100
  }))

  const values = props.radarData.map(item => item.value)

  chartInstance.setOption({
    backgroundColor: 'transparent',
    radar: {
      indicator: indicators,
      shape: 'polygon',
      splitNumber: 4,
      axisName: {
        color: '#fff',
        fontSize: 14
      },
      splitLine: {
        lineStyle: { color: 'rgba(255,255,255,0.1)' }
      },
      splitArea: {
        areaStyle: { color: ['rgba(102,126,234,0.05)', 'rgba(102,126,234,0.1)'] }
      },
      axisLine: {
        lineStyle: { color: 'rgba(255,255,255,0.15)' }
      }
    },
    series: [{
      type: 'radar',
      data: [{ value: values }],
      areaStyle: {
        color: 'rgba(102,126,234,0.3)'
      },
      lineStyle: {
        color: '#667eea',
        width: 2
      },
      itemStyle: {
        color: '#764ba2'
      }
    }]
  })
}

onMounted(initChart)
onUnmounted(() => { chartInstance?.dispose() })

watch(() => props.radarData, () => {
  updateChart()
}, { deep: true })
</script>
