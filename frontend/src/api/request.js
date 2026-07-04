/**
 * API 请求封装 —— NPFJ
 *
 * 流程：
 * 1. POST /api/session/create → 获取 session_id
 * 2. GET  /api/pool/<id>      → 获取题池题目
 * 3. POST /api/pool/<id>/submit → 提交 5 个答案（带上 session_id）
 * 4. POST /api/result          → 最终结算（带上 session_id）
 *
 * session_id 由 createSession 返回，后续每次请求都传给后端。
 * 不再依赖 cookie，避免跨域丢失会话的问题。
 */
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000
})

let _sessionId = null

/** 创建新测试会话 */
export async function createSession() {
  const res = await api.post('/session/create')
  _sessionId = res.data.session_id
  return res
}

/** 获取指定题池的题目 */
export function getPool(poolId) {
  return api.get(`/pool/${poolId}`)
}

/** 提交当前题池的 5 个答案（自动带上 session_id） */
export function submitPool(poolId, answers) {
  return api.post(`/pool/${poolId}/submit`, { session_id: _sessionId, answers })
}

/** 最终结算（自动带上 session_id） */
export function getResult() {
  return api.post('/result', { session_id: _sessionId })
}

export default api
