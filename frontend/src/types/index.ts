// ==================== 用户相关类型 ====================

export interface User {
  id: number
  username: string
  email: string | null
  created_at: string
}

// ==================== 认证相关类型 ====================

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
  email?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface RegisterResponse {
  id: number
  username: string
  email: string | null
  created_at: string
}

// ==================== 会议相关类型 ====================

export type MeetingStatus =
  | 'uploaded'
  | 'transcribing'
  | 'transcribed'
  | 'analyzing'
  | 'completed'
  | 'failed'

export type UrgencyLevel = 'high' | 'medium' | 'low'

export type TranscriptionStatus =
  | 'pending'
  | 'processing'
  | 'completed'
  | 'failed'

/** 上传处理阶段（前端 UI 概念，非后端状态） */
export type UploadStage =
  | 'idle'
  | 'uploading'
  | 'transcribing'
  | 'analyzing'
  | 'completed'
  | 'failed'

export interface TodoItem {
  task: string
  assignee: string
  deadline: string
}

export interface TranscriptionResponse {
  id: number
  meeting_id: number
  summary: string
  todos: TodoItem[]
  urgency: UrgencyLevel
  status: TranscriptionStatus
  created_at: string
}

export interface MeetingResponse {
  id: number
  filename: string
  file_size: number
  content_type: string
  status: MeetingStatus
  created_at: string
  transcription: TranscriptionResponse | null
}

export interface MeetingListResponse {
  total: number
  meetings: MeetingResponse[]
}

// ==================== Toast 通知类型 ====================

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: number
  type: ToastType
  message: string
}
