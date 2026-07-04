import request from './request'

export interface OrderListParams {
  pageNum: number
  pageSize: number
}

export function getOrderList(params: OrderListParams) {
  return request({
    url: '/order/all',
    method: 'GET',
    params,
  })
}
