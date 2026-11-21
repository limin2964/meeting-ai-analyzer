<template>
  <span
    :class="[
      'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium border',
      colorClass,
    ]"
  >
    <span class="text-sm">{{ icon }}</span>
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { UrgencyLevel } from '@/types'
import { URGENCY_LABELS, URGENCY_COLORS } from '@/utils/constants'

const props = defineProps<{
  urgency: UrgencyLevel
}>()

const label = computed(() => URGENCY_LABELS[props.urgency])
const colorClass = computed(() => URGENCY_COLORS[props.urgency])
const icon = computed(() => {
  switch (props.urgency) {
    case 'high': return '🔴'
    case 'medium': return '🟡'
    default: return '🟢'
  }
})
</script>
