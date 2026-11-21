<template>
  <span
    :class="[
      'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium',
      colorClass,
      { 'animate-pulse': isProcessing },
    ]"
  >
    <span
      v-if="isProcessing"
      class="w-1.5 h-1.5 rounded-full bg-current animate-ping"
    />
    <span v-else class="w-1.5 h-1.5 rounded-full bg-current"/>
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { MeetingStatus } from '@/types'
import { MEETING_STATUS_LABELS, MEETING_STATUS_COLORS } from '@/utils/constants'

const props = defineProps<{
  status: MeetingStatus
}>()

const label = computed(() => MEETING_STATUS_LABELS[props.status])
const colorClass = computed(() => MEETING_STATUS_COLORS[props.status])
const isProcessing = computed(() => props.status === 'transcribing' || props.status === 'analyzing')
</script>
