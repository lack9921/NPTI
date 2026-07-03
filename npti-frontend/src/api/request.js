/**
 * API 请求封装 —— 统一管理所有后端接口的调用
 * 
 * 使用 axios 库发送 HTTP 请求。
 * 开发时 Vite 会把 /api/* 的请求自动转发到后端 localhost:8080
 * （参见 vite.config.js 里的 proxy 配置）
 */
import axios from 'axios'

// 创建一个 axios 实例，设置基础 URL 和超时时间
const api = axios.create({
  baseURL: '/api',        // 所有请求前面自动加 /api
  timeout: 10000           // 10 秒超时，超过就报错
})

/** 获取所有题目（GET 请求） */
export function getQuestions() {
  return api.get('/test/questions')
}

/** 提交答案获取结果（POST 请求） */
export function submitAnswers(answers) {
  // 参数 answers 是一个数组，比如 ["A", "B", "A", ...]
  // axios.post 会自动转成 JSON 格式发给后端
  return api.post('/test/submit', { answers })
}

export default api
