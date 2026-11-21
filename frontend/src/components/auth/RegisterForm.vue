<template>
  <form @submit.prevent="handleSubmit" class="space-y-5">
    <!-- 用户名 -->
    <div>
      <label for="reg-username" class="block text-sm font-medium text-slate-700 mb-1">用户名</label>
      <input
        id="reg-username"
        v-model="username"
        type="text"
        required
        minlength="2"
        maxlength="50"
        class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors"
        placeholder="请输入用户名（2-50个字符）"
        autocomplete="username"
      />
    </div>

    <!-- 邮箱 -->
    <div>
      <label for="reg-email" class="block text-sm font-medium text-slate-700 mb-1">
        邮箱 <span class="text-slate-400 font-normal">（选填）</span>
      </label>
      <input
        id="reg-email"
        v-model="email"
        type="email"
        class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors"
        placeholder="请输入邮箱地址"
        autocomplete="email"
      />
    </div>

    <!-- 密码 -->
    <div>
      <label for="reg-password" class="block text-sm font-medium text-slate-700 mb-1">密码</label>
      <input
        id="reg-password"
        v-model="password"
        type="password"
        required
        minlength="6"
        class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors"
        placeholder="请输入密码（至少6位）"
        autocomplete="new-password"
      />
    </div>

    <!-- 错误提示 -->
    <ErrorAlert :message="authStore.error" />

    <!-- 提交按钮 -->
    <button
      type="submit"
      :disabled="authStore.isLoading"
      class="w-full bg-primary-600 text-white py-2.5 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
    >
      <span v-if="authStore.isLoading" class="flex items-center justify-center gap-2">
        <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        注册中...
      </span>
      <span v-else>注册</span>
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ErrorAlert from '@/components/common/ErrorAlert.vue'

const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')

const emit = defineEmits<{
  success: []
}>()

async function handleSubmit() {
  authStore.clearError()
  try {
    await authStore.register(username.value, password.value, email.value || undefined)
    emit('success')
  } catch {
    // 错误已在 store 中设置
  }
}
</script>
