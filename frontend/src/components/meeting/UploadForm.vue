<template>
  <div>
    <!-- 拖拽上传区域 -->
    <div
      :class="[
        'relative border-2 border-dashed rounded-xl p-10 text-center transition-all cursor-pointer',
        isDragging
          ? 'border-primary-500 bg-primary-50'
          : 'border-slate-300 hover:border-primary-400 hover:bg-slate-50',
        selectedFile && !validationError ? 'border-emerald-400 bg-emerald-50' : '',
        validationError ? 'border-red-400 bg-red-50' : '',
      ]"
      @click="triggerFileInput"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
    >
      <input
        ref="fileInput"
        type="file"
        :accept="acceptFormats"
        class="hidden"
        @change="onFileChange"
      />

      <!-- 未选择文件 -->
      <template v-if="!selectedFile">
        <svg class="w-12 h-12 text-slate-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
        </svg>
        <p class="text-slate-600 font-medium mb-1">拖拽音频文件到此处，或点击选择</p>
        <p class="text-sm text-slate-400">支持 MP3, WAV, M4A, FLAC, OGG 等格式，最大 100MB</p>
      </template>

      <!-- 已选择文件 -->
      <template v-else>
        <svg class="w-12 h-12 text-emerald-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <p class="text-slate-700 font-medium">{{ selectedFile.name }}</p>
        <p class="text-sm text-slate-500">{{ formatFileSize(selectedFile.size) }}</p>
        <button
          @click.stop="clearFile"
          class="mt-2 text-sm text-red-500 hover:text-red-700"
        >
          移除
        </button>
      </template>
    </div>

    <!-- 验证错误 -->
    <p v-if="validationError" class="mt-2 text-sm text-red-600">{{ validationError }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ALLOWED_AUDIO_EXTENSIONS } from '@/utils/constants'
import { formatFileSize } from '@/utils/format'

const props = defineProps<{
  selectedFile: File | null
  validationError: string | null
}>()

const emit = defineEmits<{
  select: [file: File]
  clear: []
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)

const acceptFormats = computed(() => ALLOWED_AUDIO_EXTENSIONS.join(','))

function triggerFileInput() {
  fileInput.value?.click()
}

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files?.length) {
    emit('select', input.files[0])
  }
}

function onDragOver() {
  isDragging.value = true
}

function onDragLeave() {
  isDragging.value = false
}

function onDrop(event: DragEvent) {
  isDragging.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) {
    emit('select', file)
  }
}

function clearFile() {
  emit('clear')
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>
