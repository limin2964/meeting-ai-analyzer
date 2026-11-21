import apiClient from './client'
import type { LoginRequest, RegisterRequest, TokenResponse, RegisterResponse, User } from '@/types'

/** 用户注册 */
export function register(data: RegisterRequest) {
  return apiClient.post<RegisterResponse>('/auth/register', data)
}

/** 用户登录 */
export function login(data: LoginRequest) {
  return apiClient.post<TokenResponse>('/auth/login', data)
}

/** 获取当前用户信息 */
export function getMe() {
  return apiClient.get<User>('/me')
}
