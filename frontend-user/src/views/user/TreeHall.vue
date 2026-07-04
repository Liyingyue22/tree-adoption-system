<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import UserHeader from '@/components/user/UserHeader.vue'
import { getTreeList } from '@/api/tree'
import { resolveImg } from '@/utils/auth'
import type { Tree } from '@/types'

const router = useRouter()

const loading = ref(false)
const treeList = ref<Tree[]>([])
const total = ref(0)
const filterStatus = ref<'' | '0' | '1'>('')

const query = reactive({
  pageNum: 1,
  pageSize: 12,
})

async function loadList() {
  loading.value = true
  try {
    console.log('当前筛选状态 filterStatus =', filterStatus.value)

    const params: any = {
      pageNum: query.pageNum,
      pageSize: query.pageSize,
    }

    if (filterStatus.value !== '') {
      params.status = Number(filterStatus.value)
    }
    
    console.log('发送给后端的参数 params =', params)
    const res = await getTreeList(params)
    console.log('树木列表返回 =', res)

    treeList.value = res.data.list ?? []
    total.value = res.data.total ?? 0
  } catch (err) {
    console.log('树木列表加载失败 =', err)
    treeList.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}


function handlePageChange(page: number) {
  query.pageNum = page
  loadList()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleFilterChange() {
  query.pageNum = 1
  loadList()
}

function goDetail(tree: Tree) {
  if (tree.status === 1) {
    ElMessage.info('该果树已被认养')
    return
  }
  router.push({ path: '/tree-detail', query: { treeId: tree.treeId } })
}

onMounted(loadList)
</script>

<template>
  <div class="tree-hall bg-paper">
    <UserHeader />

    <!-- Hero 区 -->
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-text fade-up">
          <span class="kicker">FRUIT TREE ADOPTION</span>
          <h1 class="hero-title font-serif">
            选一棵属于你的<br /><em>果树</em>
          </h1>
          <p class="hero-desc">
            每一棵果树都配备专属田间摄像头，<br />
            无论身在何处，都能见证它开花、结果、丰收。
          </p>
        </div>
        <div class="hero-stat">
          <div class="stat-item">
            <strong class="font-mono">{{ total }}</strong>
            <small>可认养果树</small>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <strong class="font-mono">24<span>h</span></strong>
            <small>实时监控</small>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <strong class="font-mono">4<span>季</span></strong>
            <small>生长可溯</small>
          </div>
        </div>
      </div>
    </section>

    <!-- 筛选区 -->
    <section class="filter-bar">
      <div class="filter-inner">
        <span class="filter-label">认养状态</span>
        <el-radio-group v-model="filterStatus" @change="handleFilterChange">
          <el-radio-button label="">全部</el-radio-button>
          <el-radio-button label="0">未认养</el-radio-button>
          <el-radio-button label="1">已认养</el-radio-button>
        </el-radio-group>
        <span class="result-count">共 <em class="font-mono">{{ total }}</em> 棵</span>
      </div>
    </section>

    <!-- 卡片列表 -->
    <section class="cards-section">
      <div class="cards-inner">
        <div v-loading="loading" class="cards-grid">
          <article
            v-for="(tree, idx) in treeList"
            :key="tree.treeId"
            class="tree-card fade-up"
            :style="{ animationDelay: `${idx * 0.04}s` }"
            @click="goDetail(tree)"
          >
            <div class="card-cover">
              <img
                v-if="tree.coverImg"
                :src="resolveImg(tree.coverImg)"
                :alt="tree.treeType"
                @error="(e) => (e.target as HTMLImageElement).style.opacity = '0'"
              />
              <div v-else class="cover-placeholder">
                <span>{{ tree.treeType?.charAt(0) || '树' }}</span>
              </div>
              <span class="status-tag" :class="tree.status === 1 ? 'adopted' : 'free'">
                {{ tree.status === 1 ? '已认养' : '未认养' }}
              </span>
            </div>

            <div class="card-body">
              <div class="card-head">
                <h3 class="tree-type font-serif">{{ tree.treeType }}</h3>
                <span class="tree-id font-mono">#{{ String(tree.treeId).padStart(4, '0') }}</span>
              </div>
              <p class="tree-position">
                <span class="loc-icon">⌖</span>{{ tree.position }}
              </p>
              <div class="card-foot">
                <div class="price">
                  <span class="unit">¥</span>
                  <span class="amount font-mono">{{ tree.price }}</span>
                  <span class="per">/ 月</span>
                </div>
                <button
                  class="action-btn"
                  :class="{ disabled: tree.status === 1 }"
                  :disabled="tree.status === 1"
                  @click.stop="goDetail(tree)"
                >
                  {{ tree.status === 1 ? '已被认养' : '查看详情' }}
                </button>
              </div>
            </div>
          </article>

          <!-- 空态 -->
          <div v-if="!loading && treeList.length === 0" class="empty-state">
            <div class="empty-icon">🌿</div>
            <p>暂无可认养的果树</p>
            <small>请稍后再来查看</small>
          </div>
        </div>

        <!-- 分页 -->
        <div v-if="total > 0" class="pagination-wrap">
          <el-pagination
            v-model:current-page="query.pageNum"
            :page-size="query.pageSize"
            :total="total"
            layout="prev, pager, next, jumper"
            background
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </section>

    <footer class="page-footer">
      <div class="leaf-divider"></div>
      <p>天子山农业公园 · 让城市与自然重新连接 · {{ new Date().getFullYear() }}</p>
    </footer>
  </div>
</template>

<style scoped lang="scss">
.tree-hall {
  min-height: 100vh;
}

/* Hero */
.hero {
  background: linear-gradient(180deg, var(--color-cream) 0%, var(--color-cream-dark) 100%);
  padding: 56px 0 48px;
  border-bottom: 1px solid rgba(31, 77, 46, 0.06);
}

.hero-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 48px;
  align-items: center;
}

.kicker {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.4em;
  color: var(--color-clay);
  font-weight: 600;
  margin-bottom: 16px;
}

.hero-title {
  font-size: 48px;
  line-height: 1.15;
  margin: 0 0 18px;
  color: var(--color-forest);
  font-weight: 600;
  letter-spacing: 0.02em;

  em {
    font-style: normal;
    color: var(--color-leaf);
    position: relative;
    &::after {
      content: '';
      position: absolute;
      left: 0;
      right: 0;
      bottom: 4px;
      height: 8px;
      background: rgba(217, 122, 61, 0.2);
      z-index: -1;
      border-radius: 4px;
    }
  }
}

.hero-desc {
  font-size: 14px;
  color: var(--color-wood);
  line-height: 1.9;
  margin: 0;
  letter-spacing: 0.02em;
}

.hero-stat {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 24px;
  padding: 28px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 18px;
  border: 1px solid rgba(31, 77, 46, 0.08);
  backdrop-filter: blur(8px);
}

.stat-item {
  text-align: center;
  strong {
    display: block;
    font-size: 32px;
    color: var(--color-forest);
    font-weight: 700;
    line-height: 1;
    span {
      font-size: 14px;
      color: var(--color-wood);
      margin-left: 2px;
    }
  }
  small {
    display: block;
    margin-top: 6px;
    font-size: 12px;
    color: var(--color-mute);
    letter-spacing: 0.1em;
  }
}

.stat-divider {
  width: 1px;
  height: 36px;
  background: rgba(31, 77, 46, 0.12);
}

/* 筛选 */
.filter-bar {
  border-bottom: 1px solid rgba(31, 77, 46, 0.06);
  background: #fff;
  position: sticky;
  top: 72px;
  z-index: 20;
}

.filter-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px 32px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.filter-label {
  font-size: 13px;
  color: var(--color-mute);
  letter-spacing: 0.1em;
}

.result-count {
  margin-left: auto;
  font-size: 13px;
  color: var(--color-wood);
  em {
    color: var(--color-clay);
    font-style: normal;
    font-weight: 600;
    margin: 0 4px;
  }
}

/* 卡片 */
.cards-section { padding: 40px 0 64px; }

.cards-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  min-height: 200px;
}

.tree-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid rgba(31, 77, 46, 0.06);
  box-shadow: var(--shadow-soft);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;

  &:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-hover);
    border-color: rgba(91, 157, 60, 0.3);

    .card-cover img { transform: scale(1.08); }
  }
}

.card-cover {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: linear-gradient(135deg, #dce8c8 0%, #b8d49a 100%);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-serif);
  font-size: 56px;
  color: rgba(31, 77, 46, 0.4);
}

.status-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 12px;
  border-radius: 14px;
  font-size: 11px;
  letter-spacing: 0.1em;
  backdrop-filter: blur(6px);

  &.free {
    background: rgba(91, 157, 60, 0.92);
    color: #fff;
  }
  &.adopted {
    background: rgba(122, 91, 58, 0.85);
    color: #fff;
  }
}

.card-body {
  padding: 18px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.card-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;

  .tree-type {
    font-size: 19px;
    color: var(--color-forest);
    margin: 0;
    font-weight: 600;
    letter-spacing: 0.02em;
  }
  .tree-id {
    font-size: 11px;
    color: var(--color-mute);
  }
}

.tree-position {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-wood);
  margin: 0;
  letter-spacing: 0.02em;

  .loc-icon { color: var(--color-clay); }
}

.card-foot {
  margin-top: auto;
  padding-top: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px dashed rgba(31, 77, 46, 0.1);
}

.price {
  display: flex;
  align-items: baseline;
  gap: 2px;
  color: var(--color-clay-deep);

  .unit { font-size: 13px; }
  .amount { font-size: 24px; font-weight: 700; }
  .per { font-size: 12px; color: var(--color-mute); }
}

.action-btn {
  padding: 8px 16px;
  border-radius: 20px;
  border: none;
  background: linear-gradient(135deg, var(--color-forest) 0%, var(--color-leaf) 100%);
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.25s ease;
  letter-spacing: 0.04em;

  &:hover:not(.disabled) {
    box-shadow: 0 4px 12px rgba(31, 77, 46, 0.3);
    transform: translateY(-1px);
  }
  &.disabled {
    background: var(--color-cream-dark);
    color: var(--color-mute);
    cursor: not-allowed;
  }
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 80px 20px;
  color: var(--color-mute);

  .empty-icon { font-size: 56px; margin-bottom: 16px; }
  p { font-size: 16px; margin: 0 0 4px; color: var(--color-wood); }
  small { font-size: 13px; }
}

.pagination-wrap {
  margin-top: 40px;
  display: flex;
  justify-content: center;
}

.page-footer {
  text-align: center;
  padding: 32px 0 40px;
  color: var(--color-mute);
  font-size: 12px;
  letter-spacing: 0.1em;

  p { margin: 16px 0 0; }
}

@media (max-width: 960px) {
  .hero-inner { grid-template-columns: 1fr; gap: 32px; }
  .hero-title { font-size: 34px; }
  .hero-stat { justify-content: center; }
}
</style>
