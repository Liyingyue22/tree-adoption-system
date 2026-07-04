import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'
import { getToken, getUserInfo } from '../utils/auth'
import { ElMessage } from 'element-plus'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/admin/login',
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/AdminLogin.vue'),
    meta: { title: '管理员登录' },
  },
  {
    path: '/admin',
    name: 'AdminLayout',
    component: () => import('../views/admin/AdminLayout.vue'),
    redirect: '/admin/tree',
    meta: { needToken: true },
    children: [
      {
        path: 'tree',
        name: 'TreeManage',
        component: () => import('../views/admin/TreeManage.vue'),
        meta: { title: '树木管理', needToken: true },
      },
      {
        path: 'order',
        name: 'OrderManage',
        component: () => import('../views/admin/OrderManage.vue'),
        meta: { title: '订单管理', needToken: true },
      },
      {
        path: 'camera',
        name: 'CameraManage',
        component: () => import('../views/admin/CameraManage.vue'),
        meta: { title: '摄像头状态', needToken: true },
      },
      {
        path: 'company',
        name: 'CompanyManage',
        component: () => import('../views/admin/CompanyManage.vue'),
        meta: { title: '公司管理', needToken: true },
      },
      {
        path: 'maintenance',
        name: 'MaintenanceManage',
        component: () => import('../views/admin/MaintenanceManage.vue'),
        meta: { title: '养护记录管理', needToken: true },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to) => {
  const token = getToken()
  const userInfo = getUserInfo()

  if (to.meta.needToken && !token) {
    ElMessage.warning('请先登录管理员账号')
    return '/admin/login'
  }

  if (to.meta.needToken && userInfo?.role !== 'admin') {
    ElMessage.error('无管理员权限')
    return '/admin/login'
  }

  if (to.path === '/admin/login' && token && userInfo?.role === 'admin') {
    return '/admin/tree'
  }

  if (to.meta.title) {
    document.title = `${to.meta.title} · 天子山管理后台`
  }

  return true
})

export default router
