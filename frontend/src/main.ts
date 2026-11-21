import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// 初始化认证状态（从 localStorage 恢复 token 和用户信息）
import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
authStore.initialize().then(() => {
  app.mount('#app')
})
