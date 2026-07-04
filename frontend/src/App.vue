<template>
  <n-config-provider :theme="darkTheme" :theme-overrides="themeOverrides">
    <n-message-provider>
      <router-view />
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
import { darkTheme } from 'naive-ui'

const themeOverrides = {
  common: {
    bodyColor: '#0f0c29',
    cardColor: 'rgba(255,255,255,0.04)',
    modalColor: '#1a1a2e',
    popoverColor: '#1a1a2e',
    primaryColor: '#667eea',
    primaryColorHover: '#7c93f5',
    primaryColorPressed: '#5568d5',
    textColor1: '#ffffff',
    textColor2: 'rgba(255,255,255,0.82)',
    textColor3: 'rgba(255,255,255,0.45)',
    borderColor: 'rgba(255,255,255,0.08)',
    dividerColor: 'rgba(255,255,255,0.06)',
    placeholderColor: 'rgba(255,255,255,0.25)',
    borderRadius: '12px',
    fontSize: '15px',
  },
  Card: {
    paddingMedium: '20px',
    borderRadius: '12px',
  },
  Button: {
    borderRadius: '12px',
    fontWeight: '600',
  },
  Steps: {
    stepHeaderSize: '14px',
    indicatorIndexFontSize: '12px',
  },
}
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; }
body {
  background: #0f0c29;
  color: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
#app { min-height: 100vh; color: #ffffff; }
</style>
