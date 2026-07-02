// 全局类型定义

export interface ApiResponse<T = unknown> {
  code: number
  msg: string
  data: T
}

export type UserRole = 'user' | 'admin'

export interface UserInfo {
  token: string
  userId: number
  username: string
  role: UserRole
  phone?: string
}

export interface Tree {
  treeId: number
  treeType: string
  position: string
  price: number
  coverImg: string
  cameraSn: string
  cameraIp: string
  camUser: string
  camPwd: string
  status: 0 | 1
  adopterId?: number
}

export interface Order {
  orderId: number
  userId: number
  username: string
  phone?: string
  treeId: number
  treeType: string
  position?: string
  cycleMonth: number
  totalPrice: number
  createTime: string
}

export interface CameraStatus {
  treeId: number
  treeType: string
  cameraSn: string
  cameraIp: string
  online: boolean
  lastHeartbeat: string
}

export interface Snapshot {
  imgUrl: string
  captureTime: string
}

export interface PageResult<T> {
  list: T[]
  total: number
}
