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
