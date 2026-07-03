<template>
  <div class="home">
    <div class="hero">
      <div class="badge">NPTI</div>
      <h1 class="title">Network Personality<br>Test Indicator</h1>
      <p class="subtitle">自创测评体系 · 4 大维度 · 16 种人格类型</p>
      <p class="desc">通过 12 道精选问题，探索你的网络人格画像</p>
      <button class="start-btn" @click="startTest">开始测试</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
function startTest() {
  router.push('/test')
}
</script>

<style scoped>
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
.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(102,126,234,0.6);
}
.start-btn:active {
  transform: translateY(0);
}
</style>
