/**
 *
 *
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