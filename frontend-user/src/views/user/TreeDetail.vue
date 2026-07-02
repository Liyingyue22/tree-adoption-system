<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import UserHeader from '@/components/user/UserHeader.vue'
import { getTreeDetail } from '@/api/tree'
import { createOrder } from '@/api/order'
import { resolveImg } from '@/utils/auth'
import type { Tree } from '@/types'

const route = useRoute()
const router = useRouter()

const tree = ref<Tree | null>(null)
const loading = ref(false)
const submitting = ref(false)

const cycleOptions = [
  { value: 3, label: '3 个月 · 季度认养' },
  { value: 6, label: '6 个月 · 半年认养' },
  { value: 12, label: '12 个月 · 全年认养' },
]
const cycleMonth = ref<number>(6)

const totalPrice = computed(() => {
  if (!tree.value) return 0
  return Number(tree.value.price) * cycleMonth.value
})

const isAdopted = computed(() => tree.value?.status === 1)

async function loadDetail() {
  const treeId = route.query.treeId as string
  if (!treeId) {
    ElMessage.error('缺少果树 ID')
    router.back()
    return
  }
  loading.value = true
  try {
    const res = await getTreeDetail(treeId)
    tree.value = res.data
    if (tree.value?.status === 1) {
      ElMessage.warning('该果树已被认养')
    }
  } catch {
    router.back()
  } finally {
    loading.value = false
  }
}

async function handleAdopt() {
  if (!tree.value || isAdopted.value) return
  try {
    await ElMessageBox.confirm(
      `确认认养「${tree.value.treeType}」${cycleMonth.value} 个月，合计 ¥${totalPrice.value}？`,
      '认养确认',
      {
        confirmButtonText: '确认认养',
        cancelButtonText: '再想想',
        type: 'info',
      },
    )
  } catch {
    return
  }

  submitting.value = true
  try {
    await createOrder({ treeId: tree.value.treeId, cycleMonth: cycleMonth.value })
    ElMessage.success('认养成功！前往我的树查看')
    router.replace('/my-tree')
  } catch {
    // 错误码 2001 已被认养等已在拦截器提示；刷新状态
    loadDetail()
  } finally {
    submitting.value = false
  }
}

function goBack() {
  router.push('/tree-hall')
}

onMounted(loadDetail)
</script>

<template>
  <div class="tree-detail bg-paper">
    <UserHeader />

    <div v-loading="loading" class="detail-wrap">
      <div v-if="tree" class="detail-inner fade-up">
        <button class="back-link" @click="goBack">
          <span>←</span> 返回认养大厅
        </button>

        <div class="detail-grid">
          <!-- 左：大图 -->
          <div class="gallery">
            <div class="main-image">
              <img
                v-if="tree.coverImg"
                :src="resolveImg(tree.coverImg)"
                :alt="tree.treeType"
              />
              <div v-else class="image-placeholder">
                <span class="font-serif">{{ tree.treeType }}</span>
              </div>
              <span class="big-status" :class="isAdopted ? 'adopted' : 'free'">
                {{ isAdopted ? '已认养' : '可认养' }}
              </span>
            </div>
            <div class="gallery-meta">
              <div class="meta-item">
                <span class="meta-label">摄像头编号</span>
                <span class="meta-value font-mono">{{ tree.cameraSn || '—' }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">设备 IP</span>
                <span class="meta-value font-mono">{{ tree.cameraIp || '—' }}</span>
              </div>
            </div>
          </div>

          <!-- 右：信息 + 下单 -->
          <div class="info-pane">
            <span class="kicker">TREE DETAIL · #{{ String(tree.treeId).padStart(4, '0') }}</span>
            <h1 class="tree-name font-serif">{{ tree.treeType }}</h1>
            <p class="tree-loc">
              <span class="loc-icon">⌖</span>{{ tree.position }}
            </p>

            <div class="leaf-divider"></div>

            <div class="intro">
              <p>
                这棵 <strong>{{ tree.treeType }}</strong> 生长于 {{ tree.position }}，
                配备专属田间摄像头，认养后可随时通过实时视频与抓拍图片观察它的生长状态，
                感受四季变化与自然节律。
              </p>
            </div>

            <div class="cycle-block">
              <h3 class="block-title">选择认养周期</h3>
              <div class="cycle-options">
                <label
                  v-for="opt in cycleOptions"
                  :key="opt.value"
                  class="cycle-item"
                  :class="{ active: cycleMonth === opt.value }"
                >
                  <input
                    v-model="cycleMonth"
                    type="radio"
                    :value="opt.value"
                    name="cycle"
                  />
                  <span class="cycle-label">{{ opt.label }}</span>
                  <span class="cycle-check">✓</span>
                </label>
              </div>
            </div>

            <div class="price-block">
              <div class="price-row">
                <span class="price-label">认养单价</span>
                <span class="price-val">
                  <em class="font-mono">¥{{ tree.price }}</em>
                  <small>/ 月</small>
                </span>
              </div>
              <div class="price-row">
                <span class="price-label">认养周期</span>
                <span class="price-val">
                  <em class="font-mono">{{ cycleMonth }}</em>
                  <small>个月</small>
                </span>
              </div>
              <div class="price-row total">
                <span class="price-label">应付总额</span>
                <span class="price-val">
                  <span class="currency">¥</span>
                  <em class="font-mono amount">{{ totalPrice.toFixed(2) }}</em>
                </span>
              </div>
            </div>

            <button
              class="adopt-btn"
              :disabled="isAdopted || submitting"
              :loading="submitting"
              @click="handleAdopt"
            >
              <span v-if="isAdopted">该果树已被认养</span>
              <span v-else-if="submitting">认养中…</span>
              <span v-else>立 即 认 养</span>
            </button>

            <p class="tips">
              <span class="tip-icon">✦</span>
              认养后可前往「我的树」查看实时监控画面与历史抓拍
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.detail-wrap {
  min-height: calc(100vh - 72px);
  padding: 32px 0 64px;
}

.detail-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  color: var(--color-wood);
  font-size: 13px;
  cursor: pointer;
  margin-bottom: 24px;
  padding: 6px 0;
  letter-spacing: 0.04em;
  transition: color 0.2s;

  &:hover { color: var(--color-forest); }
  span { font-size: 16px; }
}

.detail-grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 48px;
  align-items: start;
}

/* 左：图 */
.gallery { position: sticky; top: 96px; }

.main-image {
  position: relative;
  aspect-ratio: 4 / 3;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow-card);
  background: linear-gradient(135deg, #dce8c8 0%, #b8d49a 100%);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 64px;
  color: rgba(31, 77, 46, 0.5);
}

.big-status {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 8px 18px;
  border-radius: 22px;
  font-size: 13px;
  letter-spacing: 0.1em;
  backdrop-filter: blur(8px);

  &.free { background: rgba(91, 157, 60, 0.92); color: #fff; }
  &.adopted { background: rgba(192, 57, 43, 0.85); color: #fff; }
}

.gallery-meta {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.meta-item {
  background: #fff;
  border: 1px solid rgba(31, 77, 46, 0.08);
  border-radius: 12px;
  padding: 14px 18px;
  display: flex;
  flex-direction: column;
  gap: 4px;

  .meta-label {
    font-size: 11px;
    color: var(--color-mute);
    letter-spacing: 0.1em;
  }
  .meta-value {
    font-size: 14px;
    color: var(--color-forest);
    font-weight: 600;
  }
}

/* 右：信息 */
.info-pane {
  padding: 8px 0;
}

.kicker {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.4em;
  color: var(--color-clay);
  font-weight: 600;
  margin-bottom: 12px;
}

.tree-name {
  font-size: 40px;
  margin: 0 0 12px;
  color: var(--color-forest);
  font-weight: 600;
  letter-spacing: 0.02em;
}

.tree-loc {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  color: var(--color-wood);
  margin: 0 0 24px;
  letter-spacing: 0.02em;

  .loc-icon { color: var(--color-clay); }
}

.intro {
  margin: 24px 0 32px;
  p {
    font-size: 14px;
    line-height: 1.9;
    color: var(--color-ink);
    margin: 0;
    letter-spacing: 0.02em;
    strong { color: var(--color-forest); font-weight: 600; }
  }
}

.cycle-block { margin-bottom: 32px; }

.block-title {
  font-size: 14px;
  color: var(--color-wood);
  margin: 0 0 12px;
  font-weight: 600;
  letter-spacing: 0.06em;
}

.cycle-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cycle-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  background: #fff;
  border: 1.5px solid rgba(31, 77, 46, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;

  input { display: none; }

  .cycle-label {
    flex: 1;
    font-size: 14px;
    color: var(--color-ink);
    letter-spacing: 0.02em;
  }

  .cycle-check {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 1.5px solid rgba(31, 77, 46, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    color: transparent;
    font-size: 12px;
    transition: all 0.25s ease;
  }

  &:hover { border-color: rgba(91, 157, 60, 0.4); }

  &.active {
    border-color: var(--color-leaf);
    background: rgba(91, 157, 60, 0.06);
    .cycle-check {
      background: linear-gradient(135deg, var(--color-leaf) 0%, var(--color-forest) 100%);
      border-color: var(--color-forest);
      color: #fff;
    }
  }
}

/* 价格 */
.price-block {
  background: #fff;
  border: 1px solid rgba(31, 77, 46, 0.08);
  border-radius: 14px;
  padding: 20px 24px;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.price-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;

  .price-label { color: var(--color-mute); letter-spacing: 0.04em; }
  .price-val {
    em {
      font-style: normal;
      font-size: 16px;
      color: var(--color-ink);
      font-weight: 600;
    }
    small {
      color: var(--color-mute);
      font-size: 12px;
      margin-left: 2px;
    }
  }

  &.total {
    padding-top: 12px;
    border-top: 1px dashed rgba(31, 77, 46, 0.12);
    .price-label { color: var(--color-forest); font-weight: 600; }
    .price-val {
      color: var(--color-clay-deep);
      .currency { font-size: 18px; margin-right: 2px; }
      .amount { font-size: 28px; font-weight: 700; }
    }
  }
}

/* 认养按钮 */
.adopt-btn {
  width: 100%;
  height: 56px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--color-clay) 0%, var(--color-clay-deep) 100%);
  color: #fff;
  font-size: 16px;
  letter-spacing: 0.3em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 18px rgba(217, 122, 61, 0.3);

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(217, 122, 61, 0.4);
  }
  &:disabled {
    background: var(--color-cream-dark);
    color: var(--color-mute);
    cursor: not-allowed;
    box-shadow: none;
  }
}

.tips {
  margin: 16px 0 0;
  text-align: center;
  font-size: 12px;
  color: var(--color-mute);
  letter-spacing: 0.04em;

  .tip-icon { color: var(--color-leaf); margin-right: 4px; }
}

@media (max-width: 960px) {
  .detail-grid { grid-template-columns: 1fr; gap: 32px; }
  .gallery { position: static; }
  .tree-name { font-size: 30px; }
}
</style>
