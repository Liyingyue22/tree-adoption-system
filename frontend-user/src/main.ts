import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import '@/styles/global.scss'
import 'element-plus/theme-chalk/dark/css-vars.css'

// 开发模式启用 Mock 数据（无需后端即可调试）
// if (import.meta.env.DEV) {
//   import('@/mock').then(({ setupMock }) => setupMock())
// }

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
