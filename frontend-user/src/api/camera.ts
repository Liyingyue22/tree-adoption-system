import { request } from './request'
import type { Snapshot, CameraStatus } from '@/types'

export function getSnapshot(treeId: number | string) {
  return request<Snapshot>({
    url: '/camera/snapshot',
    method: 'GET',
    params: { treeId },
  })
}

export function getRtspUrl(treeId: number | string) {
  return request<any>({
    url: '/camera/rtsp',
    method: 'GET',
    params: { treeId },
  })
}

export function getCameraStatusList() {
  return request<CameraStatus[]>({
    url: '/camera/status/list',
    method: 'GET',
  })
}

export function manualCapture(treeId: number | string) {
  return request<Snapshot>({
    url: '/camera/manualCap',
    method: 'POST',
    data: { treeId },
  })
}
