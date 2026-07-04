<template>
  
  <div ref="chartRef" :style="{ width, height }"></div>
</template>

<script setup>
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
