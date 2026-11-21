<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-2xl font-bold text-slate-900 mb-6">📊 我的第二大脑</h1>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-xl border border-slate-200 p-6">
          <p class="text-sm text-slate-500 mb-1">总会议数</p>
          <p class="text-3xl font-bold text-slate-900">{{ meetingsStore.total }}</p>
        </div>
        <div class="bg-white rounded-xl border border-slate-200 p-6">
          <p class="text-sm text-slate-500 mb-1">已完成</p>
          <p class="text-3xl font-bold text-emerald-600">
            {{ meetingsStore.meetings.filter(m => m.status === 'completed').length }}
          </p>
        </div>
        <div class="bg-white rounded-xl border border-slate-200 p-6">
          <p class="text-sm text-slate-500 mb-1">处理中</p>
          <p class="text-3xl font-bold text-amber-600">
            {{ meetingsStore.meetings.filter(m => ['transcribing', 'analyzing', 'uploaded', 'transcribed'].includes(m.status)).length }}
          </p>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-slate-800">最近会议</h2>
        <div class="flex gap-3">
          <router-link
            to="/upload"
            class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors text-sm"
          >
            上传新会议
          </router-link>
          <router-link
            v-if="meetingsStore.total > 0"
            to="/meetings"
            class="text-primary-600 hover:text-primary-800 transition-colors text-sm flex items-center"
          >
            查看全部 →
          </router-link>
        </div>
      </div>

      <!-- 最近会议列表 -->
      <LoadingSpinner v-if="meetingsStore.isLoading" message="加载中..." />
      <EmptyState
        v-else-if="meetingsStore.meetings.length === 0"
        message="还没有会议记录"
        description="上传你的第一个会议音频文件，开始智能分析"
        action-label="上传会议"
        @action="$router.push('/upload')"
      />
      <div v-else class="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        <MeetingCard
          v-for="meeting in meetingsStore.meetings.slice(0, 6)"
          :key="meeting.id"
          :meeting="meeting"
          @click="$router.push(`/meetings/${meeting.id}`)"
        />
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useMeetingsStore } from '@/stores/meetings'
import AppLayout from '@/components/layout/AppLayout.vue'
import MeetingCard from '@/components/meeting/MeetingCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const meetingsStore = useMeetingsStore()

onMounted(() => {
  meetingsStore.fetchMeetings()
})
</script>
