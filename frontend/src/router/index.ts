import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { guest: true },
  },
  {
    path: '/meetings',
    name: 'Meetings',
    component: () => import('@/views/MeetingsView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/meetings/:id',
    name: 'MeetingDetail',
    component: () => import('@/views/MeetingDetailView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/upload',
    name: 'Upload',
    component: () => import('@/views/UploadView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫（纯状态判断，不触发网络请求）
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()

  // 已登录 → 访问登录/注册页 → 重定向到首页
  if (to.meta.guest && authStore.isAuthenticated) {
    return next('/')
  }

  // 未登录 → 访问需认证页面 → 重定向到登录页
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }

  next()
})

export default router
