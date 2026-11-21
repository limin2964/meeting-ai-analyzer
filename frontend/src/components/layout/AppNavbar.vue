<template>
  <nav class="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2 text-primary-600 font-bold text-xl">
          <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          <span>第二大脑</span>
        </router-link>

        <!-- 桌面端导航 -->
        <div class="hidden md:flex items-center gap-6">
          <template v-if="authStore.isAuthenticated">
            <router-link to="/meetings" class="text-slate-600 hover:text-primary-600 transition-colors">
              会议列表
            </router-link>
            <router-link to="/upload" class="text-slate-600 hover:text-primary-600 transition-colors">
              上传会议
            </router-link>

            <!-- 用户下拉菜单 -->
            <div class="relative" @click="toggleMenu">
              <button class="flex items-center gap-2 text-slate-700 hover:text-primary-600 transition-colors">
                <div class="w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-sm font-semibold">
                  {{ authStore.user?.username?.charAt(0).toUpperCase() }}
                </div>
                <span class="hidden lg:inline">{{ authStore.user?.username }}</span>
              </button>

              <!-- 下拉菜单 -->
              <div
                v-if="menuOpen"
                class="absolute right-0 mt-2 w-48 bg-white border border-slate-200 rounded-lg shadow-lg py-1 z-50"
                @click.stop
              >
                <div class="px-4 py-2 border-b border-slate-100">
                  <p class="text-sm font-medium text-slate-900">{{ authStore.user?.username }}</p>
                  <p class="text-xs text-slate-500">{{ authStore.user?.email || '未设置邮箱' }}</p>
                </div>
                <button
                  @click="handleLogout"
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  退出登录
                </button>
              </div>
            </div>
          </template>

          <template v-else>
            <router-link to="/login" class="text-slate-600 hover:text-primary-600 transition-colors">
              登录
            </router-link>
            <router-link
              to="/register"
              class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
            >
              注册
            </router-link>
          </template>
        </div>

        <!-- 移动端汉堡按钮 -->
        <button @click="mobileOpen = !mobileOpen" class="md:hidden text-slate-600">
          <svg v-if="!mobileOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 移动端菜单 -->
    <div v-if="mobileOpen" class="md:hidden border-t border-slate-200 bg-white px-4 py-3 space-y-2">
      <template v-if="authStore.isAuthenticated">
        <router-link to="/meetings" class="block px-3 py-2 rounded-lg text-slate-700 hover:bg-slate-50" @click="mobileOpen = false">
          会议列表
        </router-link>
        <router-link to="/upload" class="block px-3 py-2 rounded-lg text-slate-700 hover:bg-slate-50" @click="mobileOpen = false">
          上传会议
        </router-link>
        <div class="border-t border-slate-100 pt-2 mt-2">
          <p class="px-3 text-sm text-slate-500">{{ authStore.user?.username }}</p>
          <button @click="handleLogout" class="block w-full text-left px-3 py-2 rounded-lg text-red-600 hover:bg-red-50">
            退出登录
          </button>
        </div>
      </template>
      <template v-else>
        <router-link to="/login" class="block px-3 py-2 rounded-lg text-slate-700 hover:bg-slate-50" @click="mobileOpen = false">
          登录
        </router-link>
        <router-link to="/register" class="block px-3 py-2 rounded-lg text-primary-600 hover:bg-primary-50" @click="mobileOpen = false">
          注册
        </router-link>
      </template>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore, useToastStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const toastStore = useToastStore()

const menuOpen = ref(false)
const mobileOpen = ref(false)

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function handleLogout() {
  authStore.logout()
  menuOpen.value = false
  mobileOpen.value = false
  toastStore.info('已退出登录')
  router.push('/')
}

// 点击页面其他区域关闭下拉菜单
if (typeof window !== 'undefined') {
  window.addEventListener('click', () => {
    menuOpen.value = false
  })
}
</script>
