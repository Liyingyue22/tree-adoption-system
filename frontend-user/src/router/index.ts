import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getToken } from '@/utils/auth'

const routes: RouteRecordRaw[] = [
  { path: '/', redirect: '/tree-hall' },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/user/Login.vue'),
    meta: { title: '登录 / 注册' },
  },
  {
    path: '/tree-hall',
    name: 'TreeHall',
    component: () => import('@/views/user/TreeHall.vue'),
    meta: { needToken: true, title: '认养大厅' },
  },
  {
    path: '/tree-detail',
    name: 'TreeDetail',
    component: () => import('@/views/user/TreeDetail.vue'),
    meta: { needToken: true, title: '果树详情' },
  },
  {
    path: '/my-tree',
    name: 'MyTree',
    component: () => import('@/views/user/MyTree.vue'),
    meta: { needToken: true, title: '我的树' },
  },
  { path: '/:pathMatch(.*)*', redirect: '/tree-hall' },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const token = getToken()
  if (to.meta.needToken && !token) {
    ElMessage.warning('请先登录')
    return next('/login')
  }
  if (to.path === '/login' && token) {
    return next('/tree-hall')
  }
  if (to.meta.title) {
    document.title = `${to.meta.title} · 天子山农业公园`
  }
  return next()
})

export default router
