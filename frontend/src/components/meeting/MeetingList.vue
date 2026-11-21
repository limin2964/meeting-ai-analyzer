<template>
  <div class="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
    <MeetingCard
      v-for="meeting in meetings"
      :key="meeting.id"
      :meeting="meeting"
      @click="goToDetail(meeting.id)"
    />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { MeetingResponse } from '@/types'
import MeetingCard from './MeetingCard.vue'

defineProps<{
  meetings: MeetingResponse[]
}>()

const router = useRouter()

function goToDetail(id: number) {
  router.push(`/meetings/${id}`)
}
</script>
