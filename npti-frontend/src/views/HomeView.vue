<!--
  HomeView.vue —— 首页

  用户打开网站看到的第一个页面。
  显示项目名称、简介和一个大大的"开始测试"按钮。
  点击按钮跳转到答题页（/test）。
-->
<template>
  <div class="home">
    <div class="hero">
      <!-- NPTI 标志徽章 -->
      <div class="badge">NPTI</div>

      <!-- 主标题：渐变字效果 -->
      <h1 class="title">Network Personality<br>Test Indicator</h1>

      <!-- 副标题和描述 -->
      <p class="subtitle">自创测评体系 · 4 大维度 · 16 种人格类型</p>
      <p class="desc">通过 12 道精选问题，探索你的网络人格画像</p>

      <!-- 开始按钮：点击后跳转到答题页 -->
      <button class="start-btn" @click="startTest">开始测试</button>
    </div>
  </div>
</template>

<script setup>
/**
 * Vue 3 组件逻辑部分
 * <script setup> 是组合式 API，不用写 export default
 * 这里引入了 useRouter 来实现页面跳转
 */
import { useRouter } from 'vue-router'

const router = useRouter()  // 获取路由器实例

/**
 * 点击"开始测试"按钮时触发
 * router.push('/test') 让浏览器跳转到 /test 路径
 */
function startTest() {
  router.push('/test')
}
</script>

<style scoped>
/*
 * scoped 表示这些样式只对当前组件生效，
 * 不会影响到其他页面的样式。
 *
 * 页面布局：flex 居中，占满整个视口高度
 */
.home {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

.hero {
  text-align: center;
  max-width: 600px;
}

/* NPTI 徽章：半透明毛玻璃效果 */
.badge {
  display: inline-block;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  padding: 8px 24px;
  border-radius: 20px;
  font-size: 14px;
  letter-spacing: 4px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
}

/* 大标题：渐变色文字（紫色到粉色渐变） */
.title {
  font-size: 48px;
  line-height: 1.2;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 18px;
  color: rgba(255,255,255,0.7);
  margin-bottom: 12px;
}

.desc {
  font-size: 14px;
  color: rgba(255,255,255,0.5);
  margin-bottom: 40px;
}

/* 开始按钮：渐变背景 + 圆角 + 阴影 */
.start-btn {
  padding: 16px 64px;
  font-size: 18px;
  border: none;
  border-radius: 50px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 8px 32px rgba(102,126,234,0.4);
}

/* 鼠标悬停：浮起效果 */
.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(102,126,234,0.6);
}

/* 点击时：回到原位 */
.start-btn:active {
  transform: translateY(0);
}
</style>
