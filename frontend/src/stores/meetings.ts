import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { MeetingResponse, UploadStage } from '@/types'
import {
  uploadMeeting as uploadApi,
  listMeetings as listApi,
  getMeetingDetail as getDetailApi,
} from '@/api/meetings'

export const useMeetingsStore = defineStore('meetings', () => {
  // ---- 状态 ----
  const meetings = ref<MeetingResponse[]>([])
  const total = ref(0)
  const currentMeeting = ref<MeetingResponse | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // 上传状态
  const isUploading = ref(false)
  const uploadProgress = ref(0)
  const uploadStage = ref<UploadStage>('idle')
  const uploadResult = ref<MeetingResponse | null>(null)
  const uploadError = ref<string | null>(null)

  // ---- 计算属性 ----
  const meetingCount = computed(() => total.value)

  // ---- 操作 ----

  /** 获取会议列表 */
  async function fetchMeetings() {
    isLoading.value = true
    error.value = null
    try {
      const res = await listApi()
      meetings.value = res.data.meetings
      total.value = res.data.total
    } catch (e: any) {
      error.value = e.response?.data?.detail || '获取会议列表失败'
    } finally {
      isLoading.value = false
    }
  }

  /** 获取会议详情 */
  async function fetchMeetingDetail(id: number) {
    isLoading.value = true
    error.value = null
    currentMeeting.value = null
    try {
      const res = await getDetailApi(id)
      currentMeeting.value = res.data
    } catch (e: any) {
      error.value = e.response?.data?.detail || '获取会议详情失败'
    } finally {
      isLoading.value = false
    }
  }

  /** 上传会议文件 */
  async function uploadMeeting(file: File) {
    isUploading.value = true
    uploadProgress.value = 0
    uploadStage.value = 'uploading'
    uploadError.value = null
    uploadResult.value = null

    try {
      const res = await uploadApi(file, (pct) => {
        uploadProgress.value = pct
        if (pct >= 100) {
          uploadStage.value = 'transcribing'
        }
      })
      uploadResult.value = res.data
      uploadStage.value = 'completed'
      // 自动刷新会议列表
      await fetchMeetings()
    } catch (e: any) {
      uploadStage.value = 'failed'
      uploadError.value = e.response?.data?.detail || '上传失败，请重试'
    } finally {
      isUploading.value = false
    }
  }

  /** 重置上传状态 */
  function resetUpload() {
    isUploading.value = false
    uploadProgress.value = 0
    uploadStage.value = 'idle'
    uploadResult.value = null
    uploadError.value = null
  }

  /** 清除错误 */
  function clearError() {
    error.value = null
  }

  return {
    // 状态
    meetings,
    total,
    currentMeeting,
    isLoading,
    error,
    isUploading,
    uploadProgress,
    uploadStage,
    uploadResult,
    uploadError,
    // 计算属性
    meetingCount,
    // 操作
    fetchMeetings,
    fetchMeetingDetail,
    uploadMeeting,
    resetUpload,
    clearError,
  }
})
