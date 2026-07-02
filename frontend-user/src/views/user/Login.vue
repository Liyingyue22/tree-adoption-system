<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { login, register, type LoginParams, type RegisterParams } from '@/api/user'
import { useUserStore } from '@/store/user'

const router = useRouter()
const store = useUserStore()

const mode = ref<'login' | 'register'>('login')
const loading = ref(false)
const formRef = ref<FormInstance>()

const loginForm = reactive<LoginParams>({
  username: '',
  password: '',
})

const registerForm = reactive<RegisterParams>({
  username: '',
  password: '',
  phone: '',
})

const rules = computed<FormRules>(() => {
  if (mode.value === 'login') {
    return {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
    }
  }
  return {
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 3, max: 20, message: '长度 3-20 个字符', trigger: 'blur' },
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, max: 20, message: '长度 6-20 个字符', trigger: 'blur' },
    ],
    phone: [
      { required: true, message: '请输入手机号', trigger: 'blur' },
      { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' },
    ],
  }
})

function switchMode(target: 'login' | 'register') {
  mode.value = target
  formRef.value?.clearValidate()
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch {
    return
  }

  loading.value = true
  try {
    if (mode.value === 'login') {
      const res = await login({ ...loginForm })
      store.setAuth(res.data)
      ElMessage.success('登录成功，欢迎回到果园')
      router.push('/tree-hall')
    } else {
      await register({ ...registerForm })
      ElMessage.success('注册成功，请登录')
      switchMode('login')
      loginForm.username = registerForm.username
      loginForm.password = ''
    }
  } catch {
    // 错误已在拦截器中提示
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page bg-paper bg-grain">
    <!-- 左侧品牌区 -->
    <section class="brand-pane">
      <div class="brand-content">
        <div class="logo-row">
          <svg viewBox="0 0 40 40" width="44" height="44" aria-hidden="true">
            <path d="M20 3C12 7 7 14 7 22a13 13 0 0 0 26 0c0-8-5-15-13-19z" fill="#8bc34a" opacity="0.9"/>
            <path d="M20 8v26M20 17l-7-3M20 17l7-3M20 24l-6-2M20 24l6-2" stroke="#1f4d2e" stroke-width="1.6" stroke-linecap="round" fill="none"/>
          </svg>
          <span class="logo-text font-serif">天子山农业公园</span>
        </div>
        <h1 class="hero-title font-serif">
          认养一棵树<br />
          <span class="accent">守护四季的果实</span>
        </h1>
        <p class="hero-sub">
          远程认养专属果树，通过田间摄像头实时观看生长状态，<br />
          让城市生活与农业自然重新连接。
        </p>
        <div class="leaf-divider"></div>
        <ul class="feature-list">
          <li><span class="dot"></span>实时监控 · 摄像头抓拍与视频流</li>
          <li><span class="dot"></span>灵活周期 · 3 / 6 / 12 个月认养</li>
          <li><span class="dot"></span>可追溯 · 全流程订单记录</li>
        </ul>
      </div>
      <!-- 装饰叶脉 -->
      <svg class="deco-leaf" viewBox="0 0 200 200" aria-hidden="true">
        <path d="M100 20 Q160 80 100 180 Q40 80 100 20Z" fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="1.2"/>
        <path d="M100 20 L100 180 M100 60 L140 80 M100 60 L60 80 M100 100 L150 120 M100 100 L50 120 M100 140 L130 155 M100 140 L70 155" stroke="rgba(255,255,255,0.18)" stroke-width="0.8"/>
      </svg>
    </section>

    <!-- 右侧表单区 -->
    <section class="form-pane">
      <div class="form-card fade-up">
        <div class="mode-switch">
          <span :class="['switch-item', { active: mode === 'login' }]" @click="switchMode('login')">登录</span>
          <span :class="['switch-item', { active: mode === 'register' }]" @click="switchMode('register')">注册</span>
          <span class="switch-indicator" :class="{ right: mode === 'register' }"></span>
        </div>

        <h2 class="form-title font-serif">
          {{ mode === 'login' ? '欢迎回到果园' : '加入天子山农业公园，开始认养' }}
        </h2>
        <p class="form-sub">
          {{ mode === 'login' ? '使用账号登录，开启今日的远程守护' : '填写信息创建账号，即可认养专属果树' }}
        </p>

        <el-form
          ref="formRef"
          :model="mode === 'login' ? loginForm : registerForm"
          :rules="rules"
          label-position="top"
          size="large"
          @submit.prevent="handleSubmit"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="(mode === 'login' ? loginForm : registerForm).username"
              placeholder="请输入用户名"
              clearable
            >
              <template #prefix><span class="field-icon">◔</span></template>
            </el-input>
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="(mode === 'login' ? loginForm : registerForm).password"
              type="password"
              placeholder="请输入密码"
              show-password
              @keyup.enter="handleSubmit"
            >
              <template #prefix><span class="field-icon">☥</span></template>
            </el-input>
          </el-form-item>

          <el-form-item v-if="mode === 'register'" label="手机号" prop="phone">
            <el-input
              v-model="registerForm.phone"
              placeholder="请输入手机号"
              maxlength="11"
              @keyup.enter="handleSubmit"
            >
              <template #prefix><span class="field-icon">✆</span></template>
            </el-input>
          </el-form-item>

          <el-button
            type="primary"
            class="submit-btn"
            :loading="loading"
            @click="handleSubmit"
          >
            {{ mode === 'login' ? '登 录' : '注 册' }}
          </el-button>
        </el-form>

        <div class="form-foot" v-if="mode === 'login'">
          还没有账号？<el-link type="primary" :underline="false" @click="switchMode('register')">立即注册</el-link>
        </div>
        <div class="form-foot" v-else>
          已有账号？<el-link type="primary" :underline="false" @click="switchMode('login')">直接登录</el-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
}

/* 左侧品牌 */
.brand-pane {
  position: relative;
  background: linear-gradient(160deg, #1f4d2e 0%, #163a22 60%, #0e2818 100%);
  color: #fff;
  display: flex;
  align-items: center;
  padding: 64px;
  overflow: hidden;
}

.brand-content {
  position: relative;
  z-index: 2;
  max-width: 480px;
}

.logo-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 56px;

  .logo-text {
    font-size: 24px;
    letter-spacing: 0.16em;
    font-weight: 600;
  }
}

.hero-title {
  font-size: 44px;
  line-height: 1.25;
  margin: 0 0 24px;
  letter-spacing: 0.04em;
  font-weight: 600;

  .accent {
    background: linear-gradient(90deg, #8bc34a 0%, #d97a3d 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }
}

.hero-sub {
  font-size: 14px;
  line-height: 1.9;
  color: rgba(255, 255, 255, 0.72);
  margin: 0 0 32px;
  letter-spacing: 0.02em;
}

.leaf-divider {
  margin: 0 0 28px;
  filter: brightness(2);
  opacity: 0.6;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;

  li {
    display: flex;
    align-items: center;
    gap: 12px;
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    letter-spacing: 0.04em;
  }

  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #8bc34a;
    box-shadow: 0 0 8px rgba(139, 195, 74, 0.6);
  }
}

.deco-leaf {
  position: absolute;
  right: -80px;
  bottom: -80px;
  width: 360px;
  height: 360px;
  opacity: 0.4;
  animation: slow-rotate 60s linear infinite;
}

@keyframes slow-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 右侧表单 */
.form-pane {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.form-card {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 18px;
  padding: 44px 40px 36px;
  box-shadow: var(--shadow-card);
  border: 1px solid rgba(31, 77, 46, 0.06);
}

.mode-switch {
  position: relative;
  display: inline-flex;
  background: var(--color-cream);
  border-radius: 28px;
  padding: 4px;
  margin-bottom: 28px;

  .switch-item {
    position: relative;
    z-index: 2;
    padding: 8px 28px;
    font-size: 14px;
    color: var(--color-mute);
    cursor: pointer;
    transition: color 0.25s ease;
    letter-spacing: 0.06em;

    &.active { color: var(--color-forest); font-weight: 600; }
  }

  .switch-indicator {
    position: absolute;
    top: 4px;
    left: 4px;
    width: calc(50% - 4px);
    height: calc(100% - 8px);
    background: #fff;
    border-radius: 24px;
    box-shadow: 0 2px 8px rgba(31, 77, 46, 0.12);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    &.right { transform: translateX(100%); }
  }
}

.form-title {
  font-size: 24px;
  color: var(--color-ink);
  margin: 0 0 6px;
  font-weight: 600;
}

.form-sub {
  font-size: 13px;
  color: var(--color-mute);
  margin: 0 0 28px;
  letter-spacing: 0.02em;
}

.field-icon {
  display: inline-block;
  color: var(--color-wood);
  opacity: 0.7;
  font-size: 14px;
}

.submit-btn {
  width: 100%;
  height: 46px;
  margin-top: 8px;
  font-size: 15px;
  letter-spacing: 0.2em;
}

.form-foot {
  text-align: center;
  margin-top: 22px;
  font-size: 13px;
  color: var(--color-mute);
}

@media (max-width: 960px) {
  .login-page { grid-template-columns: 1fr; }
  .brand-pane {
    padding: 40px 32px;
    min-height: 240px;
  }
  .hero-title { font-size: 30px; }
  .hero-sub br { display: none; }
  .feature-list { display: none; }
  .form-pane { padding: 24px; }
  .form-card { padding: 32px 24px; }
}
</style>
