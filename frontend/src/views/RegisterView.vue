<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-blue-50 px-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center gap-2 text-primary-600 font-bold text-2xl">
          <svg class="w-10 h-10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          第二大脑
        </router-link>
        <p class="text-slate-500 mt-2">开启你的第二大脑之旅</p>
      </div>

      <!-- 注册卡片 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
        <RegisterForm @success="onRegisterSuccess" />
      </div>

      <!-- 登录链接 -->
      <p class="text-center mt-6 text-sm text-slate-500">
        已有账号？
        <router-link to="/login" class="text-primary-600 hover:text-primary-800 font-medium">
          去登录
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import RegisterForm from '@/components/auth/RegisterForm.vue'

const router = useRouter()

function onRegisterSuccess() {
  router.push('/meetings')
}
</script>
