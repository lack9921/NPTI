import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export function getQuestions() {
  return api.get('/test/questions')
}

export function submitAnswers(answers) {
  return api.post('/test/submit', { answers })
}

export default api
