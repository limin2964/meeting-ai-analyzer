<template>
  <AppLayout>
    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-2xl font-bold text-slate-900 mb-6">上传会议音频</h1>

      <!-- 未开始上传：显示拖拽区域 -->
      <template v-if="uploadStage === 'idle'">
        <UploadForm
          :selected-file="selectedFile"
          :validation-error="validationError"
          @select="onFileSelect"
          @clear="resetUpload"
        />

        <!-- 开始上传按钮 -->
        <button
          v-if="selectedFile && !validationError"
          @click="startUpload"
          class="mt-6 w-full bg-primary-600 text-white py-3 rounded-xl hover:bg-primary-700 transition-colors font-medium text-lg"
        >
          开始上传并分析
        </button>

        <p class="mt-4 text-xs text-slate-400 text-center">
          上传后将自动进行语音转文字和 AI 内容提炼，处理时间取决于音频长度
        </p>
      </template>

      <!-- 上传中 -->
      <template v-else-if="isUploading || uploadStage === 'uploading' || uploadStage === 'transcribing' || uploadStage === 'analyzing'">
        <div class="bg-white rounded-xl border border-slate-200 p-8 text-center">
          <!-- 进度条 -->
          <div class="mb-6">
            <div class="h-2 bg-slate-200 rounded-full overflow-hidden">
              <div
                :class="[
                  'h-full rounded-full transition-all duration-500',
                  uploadProgress < 100 ? 'bg-primary-500' : 'bg-primary-400 animate-pulse',
                ]"
                :style="{ width: uploadProgress + '%' }"
              />
            </div>
            <p class="text-sm text-slate-500 mt-2">
              {{ uploadProgress < 100 ? `上传中 ${uploadProgress}%` : '文件已上传，正在处理...' }}
            </p>
          </div>

          <!-- 阶段指示器 -->
          <div class="flex items-center justify-center gap-2 mb-4">
            <template v-for="(step, index) in steps" :key="step.key">
              <div class="flex flex-col items-center">
                <div
                  :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all',
                    step.active
                      ? 'bg-primary-600 text-white shadow-md'
                      : step.done
                        ? 'bg-emerald-500 text-white'
                        : 'bg-slate-200 text-slate-400',
                  ]"
                >
                  <svg v-if="step.done" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  <span v-else>{{ index + 1 }}</span>
                </div>
                <span
                  :class="[
                    'text-xs mt-1',
                    step.active ? 'text-primary-600 font-medium' : 'text-slate-400',
                  ]"
                >
                  {{ step.label }}
                </span>
              </div>
              <div
                v-if="index < steps.length - 1"
                :class="[
                  'w-12 h-0.5',
                  step.done ? 'bg-emerald-500' : 'bg-slate-200',
                ]"
              />
            </template>
          </div>

          <p class="text-slate-500 text-sm">
            {{ stageMessage }}
          </p>
        </div>
      </template>

      <!-- 上传完成 -->
      <template v-else-if="uploadStage === 'completed' && uploadResult">
        <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-8 text-center mb-6">
          <svg class="w-16 h-16 text-emerald-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <h2 class="text-xl font-bold text-emerald-800 mb-2">处理完成！</h2>
          <p class="text-emerald-600 text-sm mb-4">音频已成功转写并完成 AI 分析</p>

          <!-- 结果预览 -->
          <div v-if="uploadResult.transcription" class="text-left bg-white rounded-lg p-4 mb-4">
            <p class="text-sm font-medium text-slate-700 mb-2">📝 会议摘要</p>
            <p class="text-sm text-slate-600">{{ uploadResult.transcription.summary }}</p>

            <div class="flex items-center gap-2 mt-3">
              <span class="text-xs text-slate-500">紧急程度：</span>
              <UrgencyBadge :urgency="uploadResult.transcription.urgency" />
            </div>

            <p class="text-xs text-slate-500 mt-2">
              待办事项：{{ uploadResult.transcription.todos.length }} 项
            </p>
          </div>

          <div class="flex gap-3 justify-center">
            <router-link
              :to="`/meetings/${uploadResult.id}`"
              class="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
            >
              查看详情
            </router-link>
            <button
              @click="resetUpload"
              class="border border-slate-300 text-slate-700 px-6 py-2 rounded-lg hover:bg-slate-50 transition-colors"
            >
              再上传一个
            </button>
          </div>
        </div>
      </template>

      <!-- 上传失败 -->
      <template v-else-if="uploadStage === 'failed'">
        <div class="bg-red-50 border border-red-200 rounded-xl p-8 text-center">
          <svg class="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <h2 class="text-xl font-bold text-red-700 mb-2">处理失败</h2>
          <p class="text-red-600 text-sm mb-4">{{ uploadError || '上传或分析过程中出现错误' }}</p>
          <div class="flex gap-3 justify-center">
            <button
              @click="startUpload"
              class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-colors"
            >
              重试
            </button>
            <button
              @click="resetUpload"
              class="border border-slate-300 text-slate-700 px-6 py-2 rounded-lg hover:bg-slate-50 transition-colors"
            >
              重新选择
            </button>
          </div>
        </div>
      </template>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useMeetingsStore } from '@/stores/meetings'
import { useUpload } from '@/composables/useUpload'
import { storeToRefs } from 'pinia'
import AppLayout from '@/components/layout/AppLayout.vue'
import UploadForm from '@/components/meeting/UploadForm.vue'
import UrgencyBadge from '@/components/common/UrgencyBadge.vue'

const meetingsStore = useMeetingsStore()

const {
  selectedFile,
  validationError,
  selectFile,
  startUpload: doUpload,
  resetUpload,
} = useUpload()

// 从 store 获取上传状态
const { isUploading, uploadProgress, uploadStage, uploadResult, uploadError } =
  storeToRefs(meetingsStore)

// 阶段指示器步骤
const steps = computed(() => [
  { key: 'upload', label: '上传文件', done: uploadProgress.value >= 100, active: uploadStage.value === 'uploading' },
  { key: 'asr', label: '语音转写', done: uploadStage.value === 'analyzing' || uploadStage.value === 'completed', active: uploadStage.value === 'transcribing' },
  { key: 'llm', label: 'AI 分析', done: uploadStage.value === 'completed', active: uploadStage.value === 'analyzing' },
])

const stageMessage = computed(() => {
  switch (uploadStage.value) {
    case 'uploading': return '正在上传音频文件...'
    case 'transcribing': return '正在将语音转为文字...'
    case 'analyzing': return '正在用 AI 提炼会议内容...'
    default: return '处理中，请耐心等待...'
  }
})

function onFileSelect(file: File) {
  selectFile(file)
}

async function startUpload() {
  await doUpload()
}
</script>
