<template>
  <div class="login-page">
    <div class="login-card">
      <h1>天子山管理后台</h1>
      <p>请输入管理员账号登录</p>

      <el-form :model="form" label-position="top">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入管理员用户名" />
        </el-form-item>

        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>

        <el-button type="primary" :loading="loading" @click="handleLogin" style="width: 100%;">
          登录
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { adminLogin } from '../../api/user'
import { setToken, setUserInfo } from '../../utils/auth'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  username: 'admin01',
  password: '123456',
})

async function handleLogin() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  try {
    const res: any = await adminLogin({
      username: form.username,
      password: form.password,
    })

    if (res.data.role !== 'admin') {
      ElMessage.error('该账号不是管理员')
      return
    }

    setToken(res.data.token)
    setUserInfo(res.data)
    ElMessage.success('登录成功')
    router.push('/admin/tree')
  } catch {
    // 错误提示已经在 request.ts 里处理了
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e8f5e9, #f5f7fa);
}

.login-card {
  width: 400px;
  background: #fff;
  border-radius: 16px;
  padding: 40px 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);

  h1 {
    margin: 0 0 12px;
    font-size: 28px;
    color: #2d6a2d;
    text-align: center;
  }

  p {
    margin: 0 0 24px;
    color: #666;
    text-align: center;
  }
}
</style>
