import { request } from './request'
import type { Tree, PageResult } from '@/types'

export interface TreeListParams {
  pageNum: number
  pageSize: number
  status?: 0 | 1
}

export function getTreeList(params: TreeListParams) {
  return request<PageResult<Tree>>({
    url: '/tree/list',
    method: 'GET',
    params,
  })
}

export function getTreeDetail(treeId: number | string) {
  return request<Tree>({
    url: '/tree/detail',
    method: 'GET',
    params: { treeId },
  })
}

export function addTree(data: Partial<Tree>) {
  return request<null>({
    url: '/tree/add',
    method: 'POST',
    data,
  })
}

export function updateTree(data: Partial<Tree> & { treeId: number }) {
  return request<null>({
    url: '/tree/update',
    method: 'PUT',
    data,
  })
}

export function removeTree(treeId: number | string) {
  return request<null>({
    url: '/tree/remove',
    method: 'DELETE',
    params: { treeId },
  })
}
