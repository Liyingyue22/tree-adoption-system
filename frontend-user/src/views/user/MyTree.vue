<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import UserHeader from '@/components/user/UserHeader.vue'
import VideoPlayer from '@/components/user/VideoPlayer.vue'
import { getMyTree } from '@/api/order'
import { getSnapshot, getRtspUrl } from '@/api/camera'
import { resolveImg } from '@/utils/auth'
import type { Tree, Snapshot } from '@/types'

const router = useRouter()
const loading = ref(false)
const trees = ref<Tree[]>([])

interface TreeWithCamera extends Tree {
  imgUrl?: string
  captureTime?: string
  rtspUrl?: string
  cameraLoading?: boolean
  snapshotLoading?: boolean
  offline?: boolean
}

const cameraState = ref<Map<number, TreeWithCamera>>(new Map())

async function loadMyTrees() {
  loading.value = true
  try {
    const res = await getMyTree()
    trees.value = res.data ?? []
    // 初始化每棵树的摄像头状态
    cameraState.value = new Map(
      trees.value.map((t) => [t.treeId, { ...t }]),
    )
    // 并行加载第一棵树的监控
    if (trees.value.length > 0) {
      await loadCameraForTree(trees.value[0])
    }
  } catch {
    trees.value = []
  } finally {
    loading.value = false
  }
}

async function loadSnapshot(treeId: number) {
  const state = cameraState.value.get(treeId)
  if (!state) return
  state.snapshotLoading = true
  try {
    const res = await getSnapshot(treeId)
    state.imgUrl = res.data.imgUrl
    state.captureTime = res.data.captureTime
    state.offline = false
  } catch (err: any) {
    // 错误码 3001 摄像头离线
    if (err?.code === 3001) {
      state.offline = true
    }
  } finally {
    state.snapshotLoading = false
  }
}

async function loadRtsp(treeId: number) {
  const state = cameraState.value.get(treeId)
  if (!state) return
  state.cameraLoading = true
  try {
    const res = await getRtspUrl(treeId)
    state.rtspUrl = res.data
  } catch {
    state.rtspUrl = ''
  } finally {
    state.cameraLoading = false
  }
}

async function loadCameraForTree(tree: Tree) {
  await Promise.all([loadSnapshot(tree.treeId), loadRtsp(tree.treeId)])
}

async function handleRefresh(treeId: number) {
  await loadSnapshot(treeId)
  ElMessage.success('抓拍图已刷新')
}

function goHall() {
  router.push('/tree-hall')
}

onMounted(loadMyTrees)
</script>

<template>
  <div class="my-tree bg-paper">
    <UserHeader />

    <div class="page-head">
      <div class="head-inner">
        <div>
          <span class="kicker">MY ORCHARD</span>
          <h1 class="page-title font-serif">我的果园</h1>
          <p class="page-sub">认养的果树与它的实时状态，都在这里</p>
        </div>
        <el-button type="primary" plain @click="goHall">+ 认养更多果树</el-button>
      </div>
    </div>

    <div v-loading="loading" class="content-wrap">
      <div v-if="trees.length === 0 && !loading" class="empty-state">
        <div class="empty-icon">🌱</div>
        <p>你还没有认养任何果树</p>
        <el-button type="primary" @click="goHall">前往认养大厅</el-button>
      </div>

      <div v-else class="tree-list">
        <section
          v-for="tree in trees"
          :key="tree.treeId"
          class="tree-block fade-up"
        >
          <!-- 树信息头 -->
          <div class="block-head">
            <div class="block-head-left">
              <span class="tree-badge font-mono">#{{ String(tree.treeId).padStart(4, '0') }}</span>
              <h2 class="tree-name font-serif">{{ tree.treeType }}</h2>
              <span class="tree-pos">⌖ {{ tree.position }}</span>
            </div>
            <div class="block-head-right">
              <span class="online-dot" :class="cameraState.get(tree.treeId)?.offline ? 'offline' : 'online'"></span>
              {{ cameraState.get(tree.treeId)?.offline ? '设备离线' : '监控中' }}
            </div>
          </div>

          <!-- 监控双栏 -->
          <div class="monitor-grid">
            <!-- 抓拍图 -->
            <div class="snapshot-card">
              <div class="card-header">
                <div class="header-title">
                  <span class="title-icon">📷</span>
                  实时抓拍
                </div>
                <el-button
                  size="small"
                  :loading="cameraState.get(tree.treeId)?.snapshotLoading"
                  @click="handleRefresh(tree.treeId)"
                >
                  刷新抓拍
                </el-button>
              </div>
              <div class="snapshot-view">
                <img
                  v-if="cameraState.get(tree.treeId)?.imgUrl && !cameraState.get(tree.treeId)?.offline"
                  :src="resolveImg(cameraState.get(tree.treeId)?.imgUrl)"
                  :alt="`抓拍 ${tree.treeType}`"
                />
                <div v-else-if="cameraState.get(tree.treeId)?.offline" class="snapshot-placeholder offline">
                  <span>⚠</span>
                  <p>设备离线，暂无画面</p>
                </div>
                <div v-else class="snapshot-placeholder loading">
                  <div class="spinner"></div>
                  <p>正在获取抓拍…</p>
                </div>
              </div>
              <div class="snapshot-meta" v-if="cameraState.get(tree.treeId)?.captureTime">
                <span class="meta-label">拍摄时间</span>
                <span class="meta-value font-mono">{{ cameraState.get(tree.treeId)?.captureTime }}</span>
              </div>
            </div>

            <!-- 视频流 -->
            <div class="video-card">
              <div class="card-header">
                <div class="header-title">
                  <span class="title-icon">🎥</span>
                  实时视频
                </div>
                <span class="live-tag">
                  <span class="live-dot"></span>LIVE
                </span>
              </div>
              <VideoPlayer
                :src="cameraState.get(tree.treeId)?.rtspUrl || ''"
                :offline="cameraState.get(tree.treeId)?.offline"
                :poster="resolveImg(cameraState.get(tree.treeId)?.imgUrl)"
              />
              <div class="video-meta">
                <div class="meta-col">
                  <span class="meta-label">摄像头 SN</span>
                  <span class="meta-value font-mono">{{ tree.cameraSn || '—' }}</span>
                </div>
                <div class="meta-col">
                  <span class="meta-label">设备 IP</span>
                  <span class="meta-value font-mono">{{ tree.cameraIp || '—' }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.page-head {
  background: linear-gradient(180deg, var(--color-cream) 0%, rgba(247, 243, 236, 0.5) 100%);
  border-bottom: 1px solid rgba(31, 77, 46, 0.06);
  padding: 40px 0 32px;
}

.head-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.kicker {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.4em;
  color: var(--color-clay);
  font-weight: 600;
  margin-bottom: 8px;
}

.page-title {
  font-size: 36px;
  color: var(--color-forest);
  margin: 0 0 6px;
  font-weight: 600;
}

.page-sub {
  margin: 0;
  font-size: 14px;
  color: var(--color-wood);
  letter-spacing: 0.02em;
}

.content-wrap {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px;
  min-height: 400px;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--color-mute);

  .empty-icon { font-size: 64px; margin-bottom: 16px; }
  p { font-size: 16px; margin: 0 0 24px; color: var(--color-wood); }
}

.tree-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.tree-block {
  background: #fff;
  border: 1px solid rgba(31, 77, 46, 0.08);
  border-radius: 20px;
  padding: 28px;
  box-shadow: var(--shadow-soft);
}

.block-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 20px;
  margin-bottom: 24px;
  border-bottom: 1px solid rgba(31, 77, 46, 0.08);
}

.block-head-left {
  display: flex;
  align-items: baseline;
  gap: 14px;
  flex-wrap: wrap;

  .tree-badge {
    font-size: 12px;
    color: var(--color-mute);
    padding: 3px 10px;
    background: var(--color-cream);
    border-radius: 12px;
  }

  .tree-name {
    font-size: 26px;
    margin: 0;
    color: var(--color-forest);
    font-weight: 600;
  }

  .tree-pos {
    font-size: 13px;
    color: var(--color-wood);
    letter-spacing: 0.02em;
  }
}

.block-head-right {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-wood);

  .online-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    &.online {
      background: var(--color-online);
      box-shadow: 0 0 0 3px rgba(91, 157, 60, 0.2);
      animation: blink 1.6s infinite;
    }
    &.offline { background: var(--color-offline); }
  }
}

@keyframes blink {
  50% { opacity: 0.4; }
}

.monitor-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.snapshot-card,
.video-card {
  background: var(--color-cream);
  border-radius: 14px;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;

  .header-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: var(--color-forest);
    font-weight: 600;
    letter-spacing: 0.04em;

    .title-icon { font-size: 16px; }
  }
}

.live-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px;
  border-radius: 12px;
  background: rgba(192, 57, 43, 0.12);
  color: var(--color-offline);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;

  .live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--color-offline);
    animation: blink 1.2s infinite;
  }
}

.snapshot-view {
  position: relative;
  aspect-ratio: 16 / 9;
  background: #0d1f12;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.snapshot-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: rgba(255, 255, 255, 0.7);

  span { font-size: 36px; }
  p { margin: 0; font-size: 13px; }

  &.offline span { color: var(--color-offline); }
}

.spinner {
  width: 28px;
  height: 28px;
  border: 3px solid rgba(255, 255, 255, 0.2);
  border-top-color: var(--color-leaf);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.snapshot-meta,
.video-meta {
  margin-top: 12px;
  padding: 10px 14px;
  background: #fff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 12px;

  .meta-label {
    color: var(--color-mute);
    letter-spacing: 0.06em;
  }
  .meta-value {
    color: var(--color-forest);
    font-weight: 600;
  }
}

.video-meta {
  justify-content: flex-start;
  .meta-col {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
  }
}

@media (max-width: 960px) {
  .monitor-grid { grid-template-columns: 1fr; }
  .head-inner { flex-direction: column; align-items: flex-start; }
  .page-title { font-size: 28px; }
}
</style>
