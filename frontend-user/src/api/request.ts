import axios from 'axios'
import { ElMessage } from 'element-plus'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'
import { getToken, clearAuth } from '@/utils/auth'
import type { ApiResponse } from '@/types'

// 错误码 → 文案映射（对应文档第七章）
const ERROR_CODE_MAP: Record<number, string> = {
  1001: '账号不存在',
  1002: '密码错误',
  1003: '登录失效，请重新登录',
  2001: '果树已被认养',
  3001: '摄像头离线',
  3002: '摄像头账号密码错误',
  4001: '参数错误',
}

function redirectToLogin(): void {
  window.location.hash = '#/login'
}

const service: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

// 请求拦截：自动携带 token
service.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.token = token
    }
    return config
  },
  (error) => Promise.reject(error),
)

// 响应拦截：统一处理错误码
service.interceptors.response.use(
  (response) => {
    if (response.config.responseType === 'blob' || response.config.responseType === 'arraybuffer') {
      return response
    }
    const data = response.data as ApiResponse
    if (data.code !== 0) {
      const message = ERROR_CODE_MAP[data.code] ?? data.msg ?? '请求失败'
      if (data.code === 1003) {
        ElMessage.error(message)
        clearAuth()
        redirectToLogin()
        return Promise.reject(data)
      }
      if (data.code === 2001 || data.code === 3001) {
        ElMessage.warning(message)
        return Promise.reject(data)
      }
      ElMessage.error(message)
      return Promise.reject(data)
    }
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      clearAuth()
      redirectToLogin()
    }
    ElMessage.error(error.message || '网络异常，请稍后重试')
    return Promise.reject(error)
  },
)

// 业务请求封装：提取 response.data 为 ApiResponse<T>
export function request<T = unknown>(config: AxiosRequestConfig): Promise<ApiResponse<T>> {
  return service(config).then((res) => res.data as ApiResponse<T>)
}

export default service
