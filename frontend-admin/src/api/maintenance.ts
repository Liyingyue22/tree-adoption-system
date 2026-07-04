import request from './request'

export function getMaintenanceList() {
  return request({
    url: '/maintenance/list',
    method: 'GET',
  })
}
