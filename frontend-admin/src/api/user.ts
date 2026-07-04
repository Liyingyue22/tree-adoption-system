import request from './request'

export interface LoginParams {
  username: string
  password: string
}

export function adminLogin(data: LoginParams) {
  return request({
    url: '/user/login',
    method: 'POST',
    data,
  })
}
