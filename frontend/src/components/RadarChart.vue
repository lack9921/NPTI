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
 * 导入 Vue 的响应式 API 和 ECharts
 *
 * ref：创建一个 DOM 引用，用来获取 div 元素
 * onMounted：组件挂载后初始化图表
 * onUnmounted：组件销毁时释放图表资源
 * watch：监听数据变化，自动更新图表
 */
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  radarData: {        // 雷达图数据，格式见上方说明
    type: Array,
    default: () => []
  },
  width: {            // 图表宽度
    type: String,
    default: '100%'
  },
  height: {           // 图表高度
    type: String,
    default: '400px'
  }
})

const chartRef = ref(null)   // 图表的 DOM 容器引用
let chartInstance = null     // ECharts 实例

/** 初始化 ECharts 图表 */
function initChart() {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)  // 创建 ECharts 实例
  updateChart()  // 渲染数据
}

/** 更新图表数据 */
function updateChart() {
  if (!chartInstance || props.radarData.length === 0) return

  const indicators = props.radarData.map(item => ({
    name: item.name,  // 维度名称，如 "I/E"
    max: 100          // 最大值 100
  }))

  const values = props.radarData.map(item => item.value)

  chartInstance.setOption({
    backgroundColor: 'transparent',  // 透明背景
    radar: {
      indicator: indicators,         // 雷达图的四个轴
      shape: 'polygon',              // 多边形形状
      splitNumber: 4,                // 分成 4 圈
      axisName: {
        color: '
        fontSize: 14
      },
      splitLine: {
        lineStyle: { color: 'rgba(255,255,255,0.1)' }  // 分割线颜色
      },
      splitArea: {
        areaStyle: { color: ['rgba(102,126,234,0.05)', 'rgba(102,126,234,0.1)'] }
      },
      axisLine: {
        lineStyle: { color: 'rgba(255,255,255,0.15)' }
      }
    },
    series: [{
      type: 'radar',                 // 雷达图类型
      data: [{ value: values }],     // 数据点
      areaStyle: {
        color: 'rgba(102,126,234,0.3)'   // 填充区域颜色
      },
      lineStyle: {
        color: '
        width: 2
      },
      itemStyle: {
        color: '
      }
    }]
  })
}

onMounted(initChart)

onUnmounted(() => { chartInstance?.dispose() })

watch(() => props.radarData, () => {
  updateChart()
}, { deep: true })  // deep: true 表示深度监听（检测数组内部的变化）
</script>
