import request from './request'

export function getMaintenanceList() {
  return request({
    url: '/maintenance/list',
    method: 'GET',
  })
}

export function addMaintenance(data: any) {
  return request({
    url: '/maintenance/add',
    method: 'POST',
    data,
  })
}
