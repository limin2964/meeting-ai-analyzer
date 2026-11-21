<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 面包屑导航 -->
      <nav class="flex items-center gap-2 text-sm text-slate-500 mb-6">
        <router-link to="/meetings" class="hover:text-primary-600 transition-colors">会议列表</router-link>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
        <span class="text-slate-900">会议详情</span>
      </nav>

      <!-- 加载状态 -->
      <LoadingSpinner v-if="meetingsStore.isLoading" message="加载会议详情..." />

      <!-- 错误状态 -->
      <ErrorAlert
        v-else-if="meetingsStore.error"
        :message="meetingsStore.error"
        retry-label="重新加载"
        @retry="loadMeeting"
      />

      <!-- 会议详情 -->
      <template v-else-if="meetingsStore.currentMeeting">
        <!-- 文件信息卡片 -->
        <div class="bg-white rounded-xl border border-slate-200 p-6 mb-6">
          <div class="flex items-start justify-between mb-4">
            <div>
              <h1 class="text-xl font-bold text-slate-900 mb-1">{{ meetingsStore.currentMeeting.filename }}</h1>
              <p class="text-sm text-slate-500">{{ formatDate(meetingsStore.currentMeeting.created_at) }}</p>
            </div>
            <StatusBadge :status="meetingsStore.currentMeeting.status" />
          </div>

          <!-- 文件元信息 -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
            <div class="bg-slate-50 rounded-lg p-3">
              <p class="text-slate-400 text-xs mb-1">文件大小</p>
              <p class="font-medium text-slate-700">{{ formatFileSize(meetingsStore.currentMeeting.file_size) }}</p>
            </div>
            <div class="bg-slate-50 rounded-lg p-3">
              <p class="text-slate-400 text-xs mb-1">文件类型</p>
              <p class="font-medium text-slate-700">{{ meetingsStore.currentMeeting.content_type }}</p>
            </div>
            <div class="bg-slate-50 rounded-lg p-3">
              <p class="text-slate-400 text-xs mb-1">处理状态</p>
              <StatusBadge :status="meetingsStore.currentMeeting.status" />
            </div>
            <div class="bg-slate-50 rounded-lg p-3">
              <p class="text-slate-400 text-xs mb-1">记录 ID</p>
              <p class="font-medium text-slate-700">#{{ meetingsStore.currentMeeting.id }}</p>
            </div>
          </div>
        </div>

        <!-- 处理中/失败状态 -->
        <div
          v-if="!meetingsStore.currentMeeting.transcription && meetingsStore.currentMeeting.status !== 'completed'"
          class="bg-amber-50 border border-amber-200 rounded-xl p-6 text-center"
        >
          <svg class="w-12 h-12 text-amber-500 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <p v-if="meetingsStore.currentMeeting.status === 'failed'" class="text-amber-800 font-medium">
            处理失败
          </p>
          <p v-else class="text-amber-800 font-medium">
            正在处理中，请稍后查看...
          </p>
          <p class="text-sm text-amber-600 mt-1">
            {{ statusMessage }}
          </p>
        </div>

        <!-- 转录分析结果 -->
        <template v-if="meetingsStore.currentMeeting.transcription">
          <!-- 摘要卡片 -->
          <div class="bg-white rounded-xl border border-slate-200 p-6 mb-6">
            <h2 class="text-sm font-semibold text-slate-700 flex items-center gap-2 mb-3">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              会议摘要
            </h2>
            <p class="text-slate-700 leading-relaxed">{{ meetingsStore.currentMeeting.transcription.summary }}</p>
          </div>

          <!-- 紧急程度 + 待办事项 -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- 紧急程度 -->
            <div class="bg-white rounded-xl border border-slate-200 p-6">
              <h3 class="text-sm font-semibold text-slate-700 mb-3">紧急程度</h3>
              <UrgencyBadge :urgency="meetingsStore.currentMeeting.transcription.urgency" />
            </div>

            <!-- 待办事项 -->
            <div class="lg:col-span-2 bg-white rounded-xl border border-slate-200 p-6">
              <TodoList :todos="meetingsStore.currentMeeting.transcription.todos" />
            </div>
          </div>
        </template>
      </template>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMeetingsStore } from '@/stores/meetings'
import type { MeetingStatus } from '@/types'
import { MEETING_STATUS_LABELS } from '@/utils/constants'
import AppLayout from '@/components/layout/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import UrgencyBadge from '@/components/common/UrgencyBadge.vue'
import TodoList from '@/components/meeting/TodoList.vue'
import { formatDate, formatFileSize } from '@/utils/format'

const route = useRoute()
const meetingsStore = useMeetingsStore()

const statusMessage = computed(() => {
  const status = meetingsStore.currentMeeting?.status as MeetingStatus | undefined
  if (!status) return ''
  const label = MEETING_STATUS_LABELS[status]
  if (status === 'failed') return '语音转写或内容分析过程中出现错误，请重新上传文件'
  return `当前状态：${label}，请耐心等待处理完成`
})

function loadMeeting() {
  const id = Number(route.params.id)
  if (id) {
    meetingsStore.fetchMeetingDetail(id)
  }
}

onMounted(() => {
  loadMeeting()
})
</script>
