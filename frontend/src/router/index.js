/**
 * 路由配置 —— 决定每个 URL 显示哪个页面
 * 
 * 三个页面：
 * /        → 首页（标题 + 开始按钮）
 * /test    → 答题页（12 道题逐题作答）
 * /result  → 结果页（显示 NPTI 类型 + 雷达图）
 * 
 * createWebHistory() 表示使用干净的 URL（没有

 * 比如 http:

 */
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TestView from '../views/TestView.vue'
import ResultView from '../views/ResultView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },

  { path: '/test', name: 'Test', component: TestView },

  { path: '/result', name: 'Result', component: ResultView }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
