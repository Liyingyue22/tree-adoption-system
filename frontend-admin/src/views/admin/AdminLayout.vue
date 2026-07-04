<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="logo">天子山后台</div>

      <el-menu
        router
        :default-active="$route.path"
        class="menu"
        background-color="#1f4d2e"
        text-color="#d7e7d7"
        active-text-color="#8bc34a"
      >
        <el-menu-item index="/admin/tree">树木管理</el-menu-item>
        <el-menu-item index="/admin/order">订单管理</el-menu-item>
        <el-menu-item index="/admin/camera">摄像头状态</el-menu-item>
        <el-menu-item index="/admin/company">公司管理</el-menu-item>
        <el-menu-item index="/admin/maintenance">养护记录</el-menu-item>
      </el-menu>
    </aside>

    <div class="main-area">
      <header class="topbar">
        <span>{{ pageTitle }}</span>
        <el-button type="danger" plain size="small" @click="handleLogout">退出登录</el-button>
      </header>

      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { clearAuth } from '../../utils/auth'

const route = useRoute()
const router = useRouter()

const pageTitle = computed(() => {
  return (route.meta.title as string) || '管理后台'
})

function handleLogout() {
  clearAuth()
  ElMessage.success('已退出登录')
  router.push('/admin/login')
}
</script>

<style scoped lang="scss">
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background: #1f4d2e;
  color: #fff;
  display: flex;
  flex-direction: column;

  .logo {
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: bold;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .menu {
    border-right: none;
  }
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.topbar {
  height: 64px;
  background: #fff;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.content {
  flex: 1;
  padding: 20px;
}
</style>
