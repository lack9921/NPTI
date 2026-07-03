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
  <!-- 图表的容器 div，用 ref 引用 -->
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

// 定义组件的 props（外部传入的参数）
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

  // 构造雷达图的指标（每个维度一个指标，满分 100）
  const indicators = props.radarData.map(item => ({
    name: item.name,  // 维度名称，如 "I/E"
    max: 100          // 最大值 100
  }))

  // 提取每个维度的具体数值
  const values = props.radarData.map(item => item.value)

  // 配置 ECharts 选项
  chartInstance.setOption({
    backgroundColor: 'transparent',  // 透明背景
    radar: {
      indicator: indicators,         // 雷达图的四个轴
      shape: 'polygon',              // 多边形形状
      splitNumber: 4,                // 分成 4 圈
      axisName: {
        color: '#fff',               // 轴标签颜色
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
        color: '#667eea',            // 线条颜色
        width: 2
      },
      itemStyle: {
        color: '#764ba2'             // 数据点颜色
      }
    }]
  })
}

// 组件挂载到页面后，初始化图表
onMounted(initChart)

// 组件销毁时，释放 ECharts 实例避免内存泄漏
onUnmounted(() => { chartInstance?.dispose() })

// 监听 radarData 的变化，数据变了就重新渲染图表
watch(() => props.radarData, () => {
  updateChart()
}, { deep: true })  // deep: true 表示深度监听（检测数组内部的变化）
</script>
