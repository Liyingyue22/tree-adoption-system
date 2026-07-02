<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'

const router = useRouter()
const route = useRoute()
const store = useUserStore()

const activeName = computed(() => route.path)

async function handleLogout() {
  try {
    await ElMessageBox.confirm('确定退出登录吗？', '提示', {
      confirmButtonText: '退出',
      cancelButtonText: '取消',
      type: 'warning',
    })
    store.logout()
    router.replace('/login')
  } catch {
    // 用户取消
  }
}

function go(path: string) {
  router.push(path)
}
</script>

<template>
  <header class="user-header">
    <div class="header-inner">
      <div class="brand" @click="go('/tree-hall')">
        <span class="brand-mark">
          <svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true">
            <path d="M16 2C9 6 5 12 5 18a11 11 0 0 0 22 0c0-6-4-12-11-16z" fill="#5b9d3c" opacity="0.85"/>
            <path d="M16 6v22M16 14l-6-3M16 14l6-3M16 20l-5-2M16 20l5-2" stroke="#1f4d2e" stroke-width="1.4" stroke-linecap="round" fill="none"/>
          </svg>
        </span>
        <span class="brand-text">
          <strong class="font-serif">天子山农业公园</strong>
          <small>果树认养 · 守护一棵树</small>
        </span>
      </div>

      <nav class="nav-links">
        <span
          class="nav-item"
          :class="{ active: activeName === '/tree-hall' }"
          @click="go('/tree-hall')"
        >认养大厅</span>
        <span
          class="nav-item"
          :class="{ active: activeName === '/my-tree' }"
          @click="go('/my-tree')"
        >我的树</span>
      </nav>

      <div class="header-right">
        <div class="user-chip">
          <span class="avatar">{{ store.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
          <span class="uname">{{ store.username || '用户' }}</span>
        </div>
        <el-button text type="primary" @click="handleLogout">退出登录</el-button>
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
.user-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: linear-gradient(180deg, rgba(247, 243, 236, 0.95) 0%, rgba(247, 243, 236, 0.82) 100%);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(31, 77, 46, 0.08);
}

.header-inner {
  max-width: 1280px;
  margin: 0 auto;
  height: 72px;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;

  .brand-mark {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: rgba(91, 157, 60, 0.12);
    border-radius: 12px;
  }

  .brand-text {
    display: flex;
    flex-direction: column;
    line-height: 1.1;

    strong {
      font-size: 20px;
      color: var(--color-forest);
      letter-spacing: 0.04em;
    }
    small {
      font-size: 11px;
      color: var(--color-mute);
      letter-spacing: 0.08em;
      margin-top: 2px;
    }
  }
}

.nav-links {
  display: flex;
  gap: 8px;
  flex: 1;
  justify-content: center;

  .nav-item {
    padding: 8px 18px;
    border-radius: 24px;
    font-size: 14px;
    color: var(--color-wood);
    cursor: pointer;
    transition: all 0.25s ease;
    letter-spacing: 0.05em;

    &:hover {
      color: var(--color-forest);
      background: rgba(91, 157, 60, 0.1);
    }
    &.active {
      color: #fff;
      background: linear-gradient(135deg, var(--color-forest) 0%, var(--color-leaf) 100%);
      box-shadow: 0 4px 12px rgba(31, 77, 46, 0.25);
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 14px 4px 4px;
  background: #fff;
  border: 1px solid rgba(31, 77, 46, 0.1);
  border-radius: 24px;
  box-shadow: var(--shadow-soft);

  .avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--color-leaf) 0%, var(--color-forest) 100%);
    color: #fff;
    font-size: 13px;
    font-weight: 600;
  }

  .uname {
    font-size: 13px;
    color: var(--color-ink);
  }
}

@media (max-width: 768px) {
  .header-inner {
    padding: 0 16px;
    height: 60px;
  }
  .brand .brand-text small { display: none; }
  .nav-links .nav-item { padding: 6px 12px; font-size: 13px; }
  .user-chip .uname { display: none; }
}
</style>
