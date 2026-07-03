/**
 * 项目入口 —— 浏览器加载的第一个 JS 文件
 * 
 * 1. 创建 Vue 应用实例
 * 2. 注册路由（这样页面才能跳转）
 * 3. 加载全局样式
 * 4. 挂载到 index.html 中的 <div id="app">
 */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/style.css'

const app = createApp(App)
app.use(router)  // 注册路由
app.mount('#app')
