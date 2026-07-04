import request from './request'

export interface TreeListParams {
  pageNum: number
  pageSize: number
}

export function getTreeList(params: TreeListParams) {
  return request({
    url: '/tree/list',
    method: 'GET',
    params,
  })
}

export function addTree(data: any) {
  return request({
    url: '/tree/add',
    method: 'POST',
    data,
  })
}

export function updateTree(data: any) {
  return request({
    url: '/tree/update',
    method: 'PUT',
    data,
  })
}

export function removeTree(treeId: number) {
  return request({
    url: '/tree/remove',
    method: 'DELETE',
    params: { treeId },
  })
}
