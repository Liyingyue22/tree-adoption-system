<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import videojs from 'video.js'
import type Player from 'video.js/dist/types/player'
import 'video.js/dist/video-js.css'

const props = defineProps<{
  src: string
  /** 是否离线，离线时展示占位图 */
  offline?: boolean
  poster?: string
}>()

const videoEl = ref<HTMLVideoElement | null>(null)
const containerRef = ref<HTMLDivElement | null>(null)
let player: Player | null = null

function initPlayer() {
  if (!videoEl.value || !props.src) return
  player = videojs(videoEl.value, {
    controls: true,
    autoplay: true,
    preload: 'auto',
    fluid: true,
    liveui: true,
    poster: props.poster,
    sources: [{ src: props.src }],
  })
  player.on('error', () => {
    // 播放失败时展示提示
  })
}

function disposePlayer() {
  if (player) {
    player.dispose()
    player = null
  }
}

onMounted(() => {
  initPlayer()
})

onBeforeUnmount(() => {
  disposePlayer()
})

watch(
  () => props.src,
  (src) => {
    if (!player) {
      initPlayer()
      return
    }
    if (src) {
      player.src({ src })
      player.play?.()
    } else {
      disposePlayer()
    }
  },
)
</script>

<template>
  <div class="video-player-wrap" ref="containerRef">
    <div v-if="offline" class="offline-placeholder">
      <svg viewBox="0 0 64 64" width="48" height="48" aria-hidden="true">
        <circle cx="32" cy="32" r="28" fill="none" stroke="#c0392b" stroke-width="2" opacity="0.5"/>
        <path d="M22 22l20 20M42 22L22 42" stroke="#c0392b" stroke-width="2.5" stroke-linecap="round"/>
      </svg>
      <p>设备离线，暂无画面</p>
      <small>请稍后再试或联系管理员</small>
    </div>
    <div v-else-if="!src" class="loading-placeholder">
      <div class="pulse-dot"></div>
      <p>正在连接摄像头…</p>
    </div>
    <video
      v-show="!offline && src"
      ref="videoEl"
      class="video-js vjs-big-play-centered vjs-default-skin"
      playsinline
    />
  </div>
</template>

<style scoped lang="scss">
.video-player-wrap {
  position: relative;
  width: 100%;
  background: #0d1f12;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 16 / 9;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.05);
}

.offline-placeholder,
.loading-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  background: linear-gradient(160deg, #1a2f1f 0%, #0d1f12 100%);

  p {
    margin: 4px 0 0;
    font-size: 14px;
    letter-spacing: 0.05em;
  }
  small {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.45);
  }
}

.pulse-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-leaf);
  box-shadow: 0 0 0 0 rgba(91, 157, 60, 0.6);
  animation: pulse 1.4s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(91, 157, 60, 0.6); }
  70% { box-shadow: 0 0 0 14px rgba(91, 157, 60, 0); }
  100% { box-shadow: 0 0 0 0 rgba(91, 157, 60, 0); }
}

:deep(.video-js) {
  width: 100%;
  height: 100%;
  font-size: 13px;
}
</style>
