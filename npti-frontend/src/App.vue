<!--
  App.vue —— 根组件

  这是整个页面的最外层框架。
  <router-view /> 是一个占位符，Vue Router 会根据当前 URL
  自动在这里显示对应的页面（首页 / 答题页 / 结果页）。

  全局样式也写在这里（深色渐变背景 + 白色字体），
  所有页面都会继承这个背景。
-->
<template>
  <router-view />
</template>

<script setup>
// <script setup> 是 Vue 3 的组合式 API 写法
// 比传统的 options API 更简洁。
// 这里不需要写任何逻辑，因为根组件只负责渲染子页面。
</script>

<style>
/* 全局重置 —— 去掉浏览器默认的边距和 padding */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 页面主体：深紫色渐变背景 */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  min-height: 100vh;
  color: #fff;
}

#app {
  min-height: 100vh;
}
</style>
