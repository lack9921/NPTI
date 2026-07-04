<!--
  RadarChart.vue —— ECharts 雷达图组件

  一个可复用的 Vue 组件，用来渲染 MBTI 四维度的雷达图。
  接收雷达图数据作为 props，自动渲染 ECharts 图表。

  使用方式：
  <RadarChart :radarData="radarData" height="350px" />

  radarData 格式：
  [
    { name: "I/E", value: 56 },
    { name: "N/S", value: 67 },
    ...
  ]
-->
<template>
  <div ref="chartRef" :style="{ width, height }"></div>
</template>

<script setup>
/**
 *
 */
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  radarData: {
    type: Array,
    default: () => []
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '400px'
  }
})

const chartRef = ref(null)
let chartInstance = null

/** 初始化 ECharts 图表 */
function initChart() {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

/** 更新图表数据 */
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
        color: '#fff',
        width: 2
      },
      itemStyle: {
        color: '#fff',
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