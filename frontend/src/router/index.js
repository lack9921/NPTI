/**
 * 路由配置 —— 决定每个 URL 显示哪个页面
 * 
 * 三个页面：
 * /        → 首页（标题 + 开始按钮）
 * /test    → 答题页（12 道题逐题作答）
 * /result  → 结果页（显示 NPTI 类型 + 雷达图）
 * 
 * createWebHistory() 表示使用干净的 URL（没有 # 号）
 * 比如 http://localhost:3000/test 而不是 http://localhost:3000/#/test
 */
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TestView from '../views/TestView.vue'
import ResultView from '../views/ResultView.vue'

// 路由列表：URL 路径 → 对应的 Vue 组件
const routes = [
  { path: '/', name: 'Home', component: HomeView },       // 首页
  { path: '/test', name: 'Test', component: TestView },   // 答题页
  { path: '/result', name: 'Result', component: ResultView } // 结果页
]

// 创建路由器实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
