import request from './request'

export function getCameraStatusList() {
  return request({
    url: '/camera/status/list',
    method: 'GET',
  })
}
