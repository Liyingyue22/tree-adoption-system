import type { UserInfo, UserRole } from '@/types'

// localStorage 键名
const TOKEN_KEY = 'token'
const USER_INFO_KEY = 'userInfo'

// 兼容 SSR 与浏览器
const storage = typeof window !== 'undefined' ? window.localStorage : null

export function getToken(): string {
  return storage?.getItem(TOKEN_KEY) ?? ''
}

export function setToken(token: string): void {
  if (storage && token) storage.setItem(TOKEN_KEY, token)
}

export function removeToken(): void {
  storage?.removeItem(TOKEN_KEY)
}

export function getUserInfo(): UserInfo | null {
  if (!storage) return null
  const raw = storage.getItem(USER_INFO_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as UserInfo
  } catch {
    return null
  }
}

export function setUserInfo(info: UserInfo): void {
  if (storage && info) {
    storage.setItem(USER_INFO_KEY, JSON.stringify(info))
  }
}

export function removeUserInfo(): void {
  storage?.removeItem(USER_INFO_KEY)
}

export function getRole(): UserRole | null {
  return getUserInfo()?.role ?? null
}

export function clearAuth(): void {
  removeToken()
  removeUserInfo()
}

// 图片相对路径拼接完整域名
export function resolveImg(path?: string): string {
  if (!path) return ''
  if (/^https?:\/\//.test(path)) return path
  return `/api${path.startsWith('/') ? '' : '/'}${path}`
}
