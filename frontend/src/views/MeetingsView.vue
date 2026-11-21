<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 页头 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">会议列表</h1>
          <p class="text-sm text-slate-500 mt-1">共 {{ meetingsStore.total }} 条记录</p>
        </div>
        <router-link
          to="/upload"
          class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors text-sm flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          上传新会议
        </router-link>
      </div>

      <!-- 加载状态 -->
      <LoadingSpinner v-if="meetingsStore.isLoading" message="加载会议列表..." />

      <!-- 错误状态 -->
      <ErrorAlert
        v-else-if="meetingsStore.error"
        :message="meetingsStore.error"
        retry-label="重新加载"
        @retry="meetingsStore.fetchMeetings()"
      />

      <!-- 空状态 -->
      <EmptyState
        v-else-if="meetingsStore.meetings.length === 0"
        message="还没有会议记录"
        description="上传你的第一个会议音频文件，开始智能分析"
        action-label="上传会议"
        @action="$router.push('/upload')"
      />

      <!-- 会议列表 -->
      <MeetingList v-else :meetings="meetingsStore.meetings" />
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useMeetingsStore } from '@/stores/meetings'
import AppLayout from '@/components/layout/AppLayout.vue'
import MeetingList from '@/components/meeting/MeetingList.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const meetingsStore = useMeetingsStore()

onMounted(() => {
  meetingsStore.fetchMeetings()
})
</script>
