import request from './request'

export function getCompanyList() {
  return request({
    url: '/company/list',
    method: 'GET',
  })
}

export function addCompany(data: any) {
  return request({
    url: '/company/add',
    method: 'POST',
    data,
  })
}

export function updateCompany(data: any) {
  return request({
    url: '/company/update',
    method: 'PUT',
    data,
  })
}

export function removeCompany(companyId: number) {
  return request({
    url: '/company/remove',
    method: 'DELETE',
    params: { companyId },
  })
}
