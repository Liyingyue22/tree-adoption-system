import request from './request'

export function getCompanyList() {
  return request({
    url: '/company/list',
    method: 'GET',
  })
}
