/**
 * API 请求封装 —— NPFJ 新版 API
 *
 * 新流程：
 * 1. POST /api/session/create → 获取 session_id 和第一个题池 ID
 * 2. GET  /api/pool/<id>      → 获取当前题池的题目
 * 3. POST /api/pool/<id>/submit → 提交 5 个答案，获取路由结果
 * 4. 重复 2-3 直到 is_final = true
 * 5. POST /api/result         → 获取最终人格类型 + 五维雷达图
 *
 * 开发时 Vite 会把 /api/* 的请求自动转发到后端 localhost:8080
 */
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000
})

/** 创建新测试会话 */
export function createSession() {
  return api.post('/session/create')
}

/** 获取指定题池的题目 */
export function getPool(poolId) {
  return api.get(`/pool/${poolId}`)
}

/** 提交当前题池的 5 个答案 */
export function submitPool(poolId, answers) {
  return api.post(`/pool/${poolId}/submit`, { answers })
}

/** 最终结算，获取人格 + 五维图数据 */
export function getResult() {
  return api.post('/result')
}

export default api
