import axios from 'axios'
import { getToken, removeToken } from '@/utils/storage'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 180000, // 3 分钟默认超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器：自动注入 Bearer token
apiClient.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：统一处理 401 和错误
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      removeToken()
      // 跳转到登录页（保留当前路径作为 redirect 参数）
      const currentPath = window.location.pathname
      if (currentPath !== '/login' && currentPath !== '/register') {
        window.location.href = `/login?redirect=${encodeURIComponent(currentPath)}`
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
