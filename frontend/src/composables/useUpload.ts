import { ref } from 'vue'
import { useMeetingsStore } from '@/stores/meetings'
import { useToastStore } from '@/stores/auth'
import { ALLOWED_AUDIO_EXTENSIONS, MAX_UPLOAD_SIZE } from '@/utils/constants'
import { formatFileSize } from '@/utils/format'

export function useUpload() {
  const meetingsStore = useMeetingsStore()
  const toastStore = useToastStore()

  const selectedFile = ref<File | null>(null)
  const validationError = ref<string | null>(null)

  /** 校验文件 */
  function validateFile(file: File): string | null {
    const ext = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!ALLOWED_AUDIO_EXTENSIONS.includes(ext)) {
      return `不支持的文件格式 "${ext}"，支持的格式：${ALLOWED_AUDIO_EXTENSIONS.join(', ')}`
    }
    if (file.size > MAX_UPLOAD_SIZE) {
      return `文件过大（${formatFileSize(file.size)}），最大允许 ${formatFileSize(MAX_UPLOAD_SIZE)}`
    }
    if (file.size === 0) {
      return '文件为空，请选择有效的音频文件'
    }
    return null
  }

  /** 选择文件 */
  function selectFile(file: File) {
    validationError.value = null
    const error = validateFile(file)
    if (error) {
      validationError.value = error
      return false
    }
    selectedFile.value = file
    return true
  }

  /** 开始上传 */
  async function startUpload() {
    if (!selectedFile.value) return
    await meetingsStore.uploadMeeting(selectedFile.value)
    if (meetingsStore.uploadStage === 'completed') {
      toastStore.success('会议音频处理完成！')
    } else if (meetingsStore.uploadStage === 'failed') {
      toastStore.error(meetingsStore.uploadError || '处理失败')
    }
  }

  /** 重置上传 */
  function resetUpload() {
    selectedFile.value = null
    validationError.value = null
    meetingsStore.resetUpload()
  }

  return {
    selectedFile,
    validationError,
    selectFile,
    startUpload,
    resetUpload,
    // 从 store 暴露的上传状态
    isUploading: meetingsStore.isUploading,
    uploadProgress: meetingsStore.uploadProgress,
    uploadStage: meetingsStore.uploadStage,
    uploadResult: meetingsStore.uploadResult,
    uploadError: meetingsStore.uploadError,
  }
}
