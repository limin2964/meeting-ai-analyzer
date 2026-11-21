<template>
  <div
    class="bg-white rounded-xl border border-slate-200 p-5 hover:shadow-md transition-shadow cursor-pointer"
    @click="$emit('click')"
  >
    <div class="flex items-start justify-between mb-3">
      <div class="flex-1 min-w-0">
        <h3 class="text-base font-semibold text-slate-900 truncate">{{ meeting.filename }}</h3>
        <p class="text-xs text-slate-400 mt-1">{{ formatDate(meeting.created_at) }}</p>
      </div>
      <StatusBadge :status="meeting.status" />
    </div>

    <div class="flex items-center gap-4 text-xs text-slate-500">
      <span class="flex items-center gap-1">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        {{ meeting.content_type }}
      </span>
      <span class="flex items-center gap-1">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/>
        </svg>
        {{ formatFileSize(meeting.file_size) }}
      </span>
    </div>

    <!-- 已完成时显示摘要预览 -->
    <p
      v-if="meeting.status === 'completed' && meeting.transcription"
      class="mt-3 text-sm text-slate-500 line-clamp-2"
    >
      {{ meeting.transcription.summary }}
    </p>
  </div>
</template>

<script setup lang="ts">
import type { MeetingResponse } from '@/types'
import StatusBadge from '@/components/common/StatusBadge.vue'
import { formatDate, formatFileSize } from '@/utils/format'

defineProps<{
  meeting: MeetingResponse
}>()

defineEmits<{
  click: []
}>()
</script>
