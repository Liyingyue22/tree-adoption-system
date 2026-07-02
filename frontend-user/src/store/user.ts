import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo, UserRole } from '@/types'
import {
  getToken,
  setToken,
  removeToken,
  getUserInfo,
  setUserInfo,
  removeUserInfo,
  clearAuth,
} from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  // 初始化时从 localStorage 恢复
  const token = ref<string>(getToken())
  const userInfo = ref<UserInfo | null>(getUserInfo())

  const isLogin = computed(() => !!token.value)
  const role = computed<UserRole | null>(() => userInfo.value?.role ?? null)
  const isAdmin = computed(() => role.value === 'admin')
  const username = computed(() => userInfo.value?.username ?? '')

  function setAuth(info: UserInfo) {
    token.value = info.token
    userInfo.value = info
    setToken(info.token)
    setUserInfo(info)
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    clearAuth()
  }

  function reset() {
    logout()
  }

  return {
    token,
    userInfo,
    isLogin,
    role,
    isAdmin,
    username,
    setAuth,
    logout,
    reset,
    // 暴露给 devtools 的辅助
    removeToken,
    removeUserInfo,
  }
})
