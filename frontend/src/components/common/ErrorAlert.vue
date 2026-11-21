<template>
  <div v-if="message" class="bg-red-50 border border-red-200 rounded-lg p-4">
    <div class="flex items-start gap-3">
      <svg class="w-5 h-5 text-red-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <div class="flex-1">
        <p class="text-sm text-red-700">{{ message }}</p>
        <button
          v-if="retryLabel"
          @click="$emit('retry')"
          class="mt-2 text-sm text-red-600 hover:text-red-800 underline"
        >
          {{ retryLabel }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: string | null
  retryLabel?: string
}>()

defineEmits<{
  retry: []
}>()
</script>
