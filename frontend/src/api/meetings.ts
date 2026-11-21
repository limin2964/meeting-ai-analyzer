import apiClient from './client'
import type { MeetingResponse, MeetingListResponse } from '@/types'

/** 上传会议音频文件 */
export function uploadMeeting(
  file: File,
  onProgress?: (pct: number) => void
) {
  const formData = new FormData()
  formData.append('file', file)
  return apiClient.post<MeetingResponse>('/meetings/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 300000, // 5 分钟超时（包含 ASR + LLM 处理时间）
    onUploadProgress: (event) => {
      if (event.total && onProgress) {
        onProgress(Math.round((event.loaded * 100) / event.total))
      }
    },
  })
}

/** 获取会议列表 */
export function listMeetings() {
  return apiClient.get<MeetingListResponse>('/meetings/list_meetings')
}

/** 获取会议详情 */
export function getMeetingDetail(id: number) {
  return apiClient.get<MeetingResponse>(`/meetings/get_meeting/${id}`)
}
