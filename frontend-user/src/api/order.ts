import { request } from './request'
import type { Tree, Order, PageResult } from '@/types'

export interface CreateOrderParams {
  treeId: number | string
  cycleMonth: number
}

export interface OrderListParams {
  pageNum: number
  pageSize: number
}

export function createOrder(params: CreateOrderParams) {
  return request<{ orderId: number }>({
    url: '/order/create',
    method: 'POST',
    data: params,
  })
}

export function getMyTree() {
  return request<Tree[]>({
    url: '/order/myTree',
    method: 'GET',
  })
}

export function getAllOrders(params: OrderListParams) {
  return request<PageResult<Order>>({
    url: '/order/all',
    method: 'GET',
    params,
  })
}
