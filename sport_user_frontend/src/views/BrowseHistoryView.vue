<template>
  <div class="page">
    <div class="mobile-shell">
      <div class="top-bar">
        <van-icon name="arrow-left" size="20" @click="goBack" />
        <span class="top-title">浏览记录</span>
        <span class="top-placeholder"></span>
      </div>

      <div v-if="loading" class="loading-wrap">
        <van-loading size="24px" vertical>加载中...</van-loading>
      </div>

      <van-empty
        v-else-if="historyList.length === 0"
        image="underway-o"
        description="暂无浏览记录"
      />

      <div v-else class="card-list">
        <div
          v-for="item in historyList"
          :key="item.id"
          class="product-card"
          @click="goDetail(item.product.id)"
        >
          <div class="image-wrap">
            <img
              :src="item.product.main_image || defaultImage"
              :alt="item.product.name"
              class="product-image"
            />
          </div>

          <div class="product-info">
            <div class="product-name van-multi-ellipsis--l2">
              {{ item.product.name }}
            </div>

            <div class="meta-row">
              <span>{{ item.product.brand || '未标注品牌' }}</span>
              <span>{{ item.product.category_name || '未分类' }}</span>
            </div>

            <div class="price-row">
              <span class="price-text">¥{{ formatPrice(item.product.price) }}</span>
              <span class="time-text">{{ formatDateTime(item.viewed_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-safe-space"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast } from 'vant'
import { getBrowseHistoryListApi, type BrowseHistoryItem } from '@/api/recommend'

const router = useRouter()

const loading = ref(false)
const historyList = ref<BrowseHistoryItem[]>([])

const defaultImage = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

function goBack() {
  router.back()
}

function goDetail(id: number) {
  router.push(`/product/${id}`)
}

function formatPrice(value: string | number) {
  return Number(value || 0).toFixed(2)
}

function formatDateTime(value: string) {
  if (!value) return ''
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const mi = String(date.getMinutes()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd} ${hh}:${mi}`
}

async function fetchHistoryList() {
  try {
    loading.value = true
    const res = await getBrowseHistoryListApi()
    historyList.value = res.data || []
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '获取浏览记录失败',
    )
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchHistoryList()
})
</script>

<style scoped>
.page { min-height: 100vh; background: #f5f7fa; }
.mobile-shell { width: 100%; max-width: 420px; min-height: 100vh; margin: 0 auto; background: #f5f7fa; }
.top-bar {
  position: sticky; top: 0; z-index: 20; height: 46px; padding: 0 14px;
  background: rgba(255,255,255,.96); display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid #edf1f5; backdrop-filter: blur(10px);
}
.top-title { font-size: 16px; font-weight: 700; color: #1f2d3d; }
.top-placeholder { width: 20px; }
.loading-wrap { min-height: 60vh; display: flex; align-items: center; justify-content: center; }
.card-list { padding: 12px; display: flex; flex-direction: column; gap: 12px; }
.product-card {
  display: flex; gap: 12px; padding: 12px; border-radius: 18px; background: #fff;
  box-shadow: 0 4px 14px rgba(31,45,61,.05);
}
.image-wrap { width: 96px; min-width: 96px; height: 96px; border-radius: 14px; overflow: hidden; background: #f3f5f7; }
.product-image { width: 100%; height: 100%; object-fit: cover; }
.product-info { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.product-name { font-size: 15px; font-weight: 700; color: #1f2d3d; line-height: 1.45; }
.meta-row { margin-top: 8px; display: flex; justify-content: space-between; gap: 8px; color: #7b8794; font-size: 12px; }
.price-row { margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; }
.price-text { color: #ee0a24; font-size: 18px; font-weight: 700; }
.time-text { font-size: 12px; color: #98a2b3; }
.bottom-safe-space { height: 24px; }
</style>