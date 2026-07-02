import { request } from './request'
import type { UserInfo } from '@/types'

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  password: string
  phone: string
}

export function login(params: LoginParams) {
  return request<UserInfo>({
    url: '/user/login',
    method: 'POST',
    data: params,
  })
}

export function register(params: RegisterParams) {
  return request<null>({
    url: '/user/register',
    method: 'POST',
    data: params,
  })
}
