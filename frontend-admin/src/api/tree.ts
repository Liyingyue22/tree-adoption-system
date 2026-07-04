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

export function removeTree(treeId: number) {
  return request({
    url: '/tree/remove',
    method: 'DELETE',
    params: { treeId },
  })
}
