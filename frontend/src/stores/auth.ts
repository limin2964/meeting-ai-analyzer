import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, Toast, ToastType } from '@/types'
import { getToken, setToken, removeToken } from '@/utils/storage'
import { login as loginApi, register as registerApi, getMe } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // ---- 状态 ----
  const token = ref<string | null>(getToken())
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // ---- 计算属性 ----
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  // ---- 操作 ----

  /** 初始化：从 localStorage 恢复登录态 */
  async function initialize() {
    if (!token.value) return
    isLoading.value = true
    error.value = null
    try {
      const res = await getMe()
      user.value = res.data
    } catch {
      // Token 无效或过期
      token.value = null
      removeToken()
    } finally {
      isLoading.value = false
    }
  }

  /** 登录 */
  async function login(username: string, password: string) {
    isLoading.value = true
    error.value = null
    try {
      const res = await loginApi({ username, password })
      token.value = res.data.access_token
      setToken(res.data.access_token)

      // 获取用户信息
      const userRes = await getMe()
      user.value = userRes.data
    } catch (e: any) {
      const detail = e.response?.data?.detail || '登录失败，请检查用户名和密码'
      error.value = detail
      throw new Error(detail)
    } finally {
      isLoading.value = false
    }
  }

  /** 注册 */
  async function register(username: string, password: string, email?: string) {
    isLoading.value = true
    error.value = null
    try {
      await registerApi({ username, password, email })
      // 注册成功后自动登录
      await login(username, password)
    } catch (e: any) {
      const detail = e.response?.data?.detail || '注册失败，请稍后重试'
      error.value = detail
      throw new Error(detail)
    } finally {
      isLoading.value = false
    }
  }

  /** 退出登录 */
  function logout() {
    token.value = null
    user.value = null
    removeToken()
  }

  /** 清除错误 */
  function clearError() {
    error.value = null
  }

  return {
    // 状态
    token,
    user,
    isLoading,
    error,
    // 计算属性
    isAuthenticated,
    // 操作
    initialize,
    login,
    register,
    logout,
    clearError,
  }
})

// ==================== Toast Store ====================

export const useToastStore = defineStore('toast', () => {
  const messages = ref<Toast[]>([])
  let nextId = 0

  function addToast(type: ToastType, message: string) {
    const id = nextId++
    messages.value.push({ id, type, message })
    setTimeout(() => {
      removeToast(id)
    }, 3000)
  }

  function removeToast(id: number) {
    messages.value = messages.value.filter((t) => t.id !== id)
  }

  function success(message: string) {
    addToast('success', message)
  }
  function error(message: string) {
    addToast('error', message)
  }
  function warning(message: string) {
    addToast('warning', message)
  }
  function info(message: string) {
    addToast('info', message)
  }

  return { messages, addToast, removeToast, success, error, warning, info }
})
