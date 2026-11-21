<template>
  <div class="min-h-screen flex flex-col">
    <AppNavbar />
    <main class="flex-1">
      <slot />
    </main>
    <!-- 页脚 -->
    <footer class="bg-white border-t border-slate-200 py-6 mt-auto">
      <div class="max-w-7xl mx-auto px-4 text-center text-sm text-slate-400">
        第二大脑 &copy; {{ new Date().getFullYear() }} — 你的 AI 会议记忆中枢
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import AppNavbar from './AppNavbar.vue'
</script>
