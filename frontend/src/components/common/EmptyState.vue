<template>
  <div class="flex flex-col items-center justify-center py-16 text-center">
    <svg class="w-20 h-20 text-slate-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
        d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
    </svg>
    <h3 class="text-lg font-medium text-slate-600 mb-2">{{ message }}</h3>
    <p v-if="description" class="text-sm text-slate-400 mb-4">{{ description }}</p>
    <button
      v-if="actionLabel"
      @click="$emit('action')"
      class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors text-sm"
    >
      {{ actionLabel }}
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: string
  description?: string
  actionLabel?: string
}>()

defineEmits<{
  action: []
}>()
</script>
