import type { MeetingStatus, UrgencyLevel } from '@/types'

/** 会议状态中文映射 */
export const MEETING_STATUS_LABELS: Record<MeetingStatus, string> = {
  uploaded: '已上传',
  transcribing: '转写中',
  transcribed: '已转写',
  analyzing: '分析中',
  completed: '已完成',
  failed: '失败',
}

/** 会议状态对应颜色 */
export const MEETING_STATUS_COLORS: Record<MeetingStatus, string> = {
  uploaded: 'bg-gray-100 text-gray-700',
  transcribing: 'bg-blue-100 text-blue-700',
  transcribed: 'bg-indigo-100 text-indigo-700',
  analyzing: 'bg-purple-100 text-purple-700',
  completed: 'bg-emerald-100 text-emerald-700',
  failed: 'bg-red-100 text-red-700',
}

/** 紧急程度中文映射 */
export const URGENCY_LABELS: Record<UrgencyLevel, string> = {
  high: '高',
  medium: '中',
  low: '低',
}

/** 紧急程度对应颜色 */
export const URGENCY_COLORS: Record<UrgencyLevel, string> = {
  high: 'bg-red-100 text-red-700 border-red-300',
  medium: 'bg-amber-100 text-amber-700 border-amber-300',
  low: 'bg-emerald-100 text-emerald-700 border-emerald-300',
}

/** 支持的上传文件扩展名 */
export const ALLOWED_AUDIO_EXTENSIONS = [
  '.mp3', '.wav', '.m4a', '.aac',
  '.ogg', '.flac', '.wma', '.webm', '.opus',
]

/** 最大上传文件大小 (100 MB) */
export const MAX_UPLOAD_SIZE = 100 * 1024 * 1024
