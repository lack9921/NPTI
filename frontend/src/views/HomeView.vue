<template>
  <div class="home">
    <div class="hero">
      <n-gradient-text type="info" :size="14" class="badge-text" v-if="false">NPFJ</n-gradient-text>
      <div class="logo-badge">NPFJ</div>
      <h1 class="title">
        <n-gradient-text :size="44" type="info">Network Personality</n-gradient-text><br>
        <n-gradient-text :size="44" type="warning">Test Indicator</n-gradient-text>
      </h1>
      <p class="subtitle">自创测评体系 · 4 大维度 · 16 种人格类型</p>
      <p class="desc">通过动态路由二分树，探索你的网络人格画像</p>
      <n-button type="primary" size="large" round :strong="true" @click="startTest"
        style="padding: '0 48px'; height: 50px; font-size: 17px;">
        开始测试
      </n-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
function startTest() { router.push('/test') }
</script>

<style scoped>
.home {
  display: flex; align-items: center; justify-content: center;
  min-height: 100vh; padding: 20px;
}
.hero { text-align: center; max-width: 600px; }
.logo-badge {
  display: inline-block;
  background: rgba(102,126,234,0.12);
  border: 1px solid rgba(102,126,234,0.25);
  color: #667eea;
  padding: 6px 22px;
  border-radius: 20px;
  font-size: 14px;
  letter-spacing: 5px;
  margin-bottom: 28px;
}
.title { line-height: 1.3; margin-bottom: 18px; }
.subtitle { font-size: 17px; color: rgba(255,255,255,0.6); margin-bottom: 10px; }
.desc { font-size: 14px; color: rgba(255,255,255,0.35); margin-bottom: 36px; }
</style>