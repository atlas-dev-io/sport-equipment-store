<template>
  <div class="page">
    <div class="mobile-shell">
      <div class="top-bar">
        <van-icon name="arrow-left" size="20" @click="goBack" />
        <span class="top-title">商品详情</span>
        <van-icon name="home-o" size="20" @click="goHome" />
      </div>

      <div v-if="loading" class="loading-wrap">
        <van-loading size="24px" vertical>加载中...</van-loading>
      </div>

      <van-empty
        v-else-if="!product"
        image="error"
        description="商品不存在或加载失败"
      />

      <template v-else>
        <div class="image-section">
          <van-swipe
            class="product-swipe"
            :autoplay="3000"
            indicator-color="#1989fa"
            lazy-render
          >
            <van-swipe-item
              v-for="img in displayImages"
              :key="img.id"
            >
              <img
                :src="img.image_url || product.main_image || defaultImage"
                :alt="img.alt_text || product.name"
                class="banner-image"
              />
            </van-swipe-item>
          </van-swipe>
        </div>

        <div class="info-card">
          <div class="price-row">
            <div class="left-price">
              <span class="currency">¥</span>
              <span class="sale-price">{{ formatPrice(product.price) }}</span>
              <span
                v-if="showMarketPrice(product.market_price, product.price)"
                class="market-price"
              >
                ¥{{ formatPrice(product.market_price) }}
              </span>
            </div>

            <div class="sales-text">销量 {{ product.sales_count }}</div>
          </div>

          <div class="product-name">
            {{ product.name }}
          </div>

          <div v-if="product.subtitle" class="product-subtitle">
            {{ product.subtitle }}
          </div>

          <div class="tag-row">
            <span v-if="product.is_recommend" class="tag tag--recommend">推荐商品</span>
            <span class="tag">{{ product.brand || '未标注品牌' }}</span>
            <span class="tag">{{ product.category?.name || '未分类' }}</span>
            <span class="tag">库存 {{ product.stock }}</span>
          </div>
        </div>

        <div class="detail-card">
          <div class="section-title">商品信息</div>

          <div class="info-list">
            <div class="info-item">
              <span class="label">商品名称</span>
              <span class="value">{{ product.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">品牌</span>
              <span class="value">{{ product.brand || '未标注' }}</span>
            </div>
            <div class="info-item">
              <span class="label">SKU</span>
              <span class="value">{{ product.sku || '暂无' }}</span>
            </div>
            <div class="info-item">
              <span class="label">分类</span>
              <span class="value">{{ product.category?.name || '未分类' }}</span>
            </div>
            <div class="info-item">
              <span class="label">商家</span>
              <span class="value">{{ product.merchant_username || '平台自营' }}</span>
            </div>
            <div class="info-item">
              <span class="label">状态</span>
              <span class="value">{{ formatStatus(product.status) }}</span>
            </div>
          </div>
        </div>

        <div class="detail-card">
          <div class="section-title">商品介绍</div>
          <div class="description-content">
            {{ product.description || '暂无商品介绍' }}
          </div>
        </div>

        <div class="bottom-safe-space"></div>

        <div class="bottom-action">
          <div class="action-left" @click="goHome">
            <van-icon name="shop-o" size="20" />
            <span>首页</span>
          </div>

          <div class="action-left" @click="goLogin">
            <van-icon name="contact-o" size="20" />
            <span>{{ isLogin ? '我的' : '登录' }}</span>
          </div>

          <div class="action-left" @click="handleToggleFavorite">
            <van-icon :name="isFavorite ? 'star' : 'star-o'" size="20" />
            <span>{{ isFavorite ? '已收藏' : '收藏' }}</span>
          </div>

          <van-button
            round
            plain
            type="primary"
            class="cart-btn"
            @click="handleAddToCart"
          >
            加入购物车
          </van-button>

          <van-button
            round
            type="primary"
            class="buy-btn"
            @click="handleBuyNow"
          >
            立即购买
          </van-button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showFailToast, showSuccessToast } from 'vant'
import { getProductDetailApi, type ProductDetail, type ProductImageItem } from '@/api/product'
import { addCartItemApi } from '@/api/cart'
import {
  getFavoriteStatusApi,
  recordBrowseHistoryApi,
  toggleFavoriteApi,
} from '@/api/recommend'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loading = ref(false)
const product = ref<ProductDetail | null>(null)
const isFavorite = ref(false)

const defaultImage = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

const isLogin = computed(() => userStore.isLogin)

const displayImages = computed<ProductImageItem[]>(() => {
  if (!product.value) return []

  if (product.value.images && product.value.images.length > 0) {
    return product.value.images
  }

  return [
    {
      id: 0,
      image_url: product.value.main_image || defaultImage,
      alt_text: product.value.name,
      sort_order: 0,
      is_main: true,
      created_at: '',
    },
  ]
})

function formatPrice(value: string | number) {
  const num = Number(value || 0)
  return num.toFixed(2)
}

function showMarketPrice(marketPrice: string | number, salePrice: string | number) {
  return Number(marketPrice) > Number(salePrice)
}

function formatStatus(status: string) {
  const map: Record<string, string> = {
    draft: '草稿',
    on_sale: '上架中',
    off_sale: '已下架',
  }
  return map[status] || status || '未知'
}

function goBack() {
  router.back()
}

function goHome() {
  router.push('/')
}

function goLogin() {
  if (isLogin.value) {
    router.push('/profile')
  } else {
    router.push('/login')
  }
}

function goLoginWithRedirect() {
  router.push({
    path: '/login',
    query: {
      redirect: route.fullPath,
    },
  })
}

async function syncUserBehavior(productId: number) {
  if (!isLogin.value) {
    isFavorite.value = false
    return
  }

  try {
    await recordBrowseHistoryApi(productId)
  } catch {
    // 浏览记录失败不阻断页面
  }

  try {
    const res = await getFavoriteStatusApi(productId)
    isFavorite.value = !!res.data?.is_favorite
  } catch {
    isFavorite.value = false
  }
}

async function handleToggleFavorite() {
  if (!isLogin.value) {
    showFailToast('请先登录后再收藏')
    goLoginWithRedirect()
    return
  }

  if (!product.value) {
    showFailToast('商品信息异常')
    return
  }

  try {
    const res = await toggleFavoriteApi(product.value.id)
    isFavorite.value = !!res.data?.is_favorite
    showSuccessToast(res.message || (isFavorite.value ? '收藏成功' : '取消收藏成功'))
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '收藏操作失败',
    )
  }
}

async function handleAddToCart() {
  if (!isLogin.value) {
    showFailToast('请先登录后再加入购物车')
    goLoginWithRedirect()
    return
  }

  if (!product.value) {
    showFailToast('商品信息异常')
    return
  }

  try {
    await addCartItemApi({
      product_id: product.value.id,
      quantity: 1,
    })

    showSuccessToast('加入购物车成功')
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '加入购物车失败',
    )
  }
}

function handleBuyNow() {
  if (!isLogin.value) {
    showFailToast('请先登录后再购买')
    goLoginWithRedirect()
    return
  }

  router.push('/checkout')
}

async function fetchProductDetail(id: string | number) {
  if (!id) return

  try {
    loading.value = true
    const res = await getProductDetailApi(id)
    product.value = res.data

    if (product.value) {
      await syncUserBehavior(product.value.id)
    }
  } catch (error: any) {
    product.value = null
    isFavorite.value = false
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '获取商品详情失败',
    )
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProductDetail(route.params.id as string)
})

watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      fetchProductDetail(newId as string)
    }
  },
)
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f7fa;
}

.mobile-shell {
  width: 100%;
  max-width: 420px;
  min-height: 100vh;
  margin: 0 auto;
  background: #f5f7fa;
}

.top-bar {
  position: sticky;
  top: 0;
  z-index: 20;
  height: 46px;
  padding: 0 14px;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #edf1f5;
  backdrop-filter: blur(10px);
}

.top-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2d3d;
}

.loading-wrap {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-section {
  background: #fff;
}

.product-swipe {
  height: 320px;
  background: #f3f5f7;
}

.banner-image {
  width: 100%;
  height: 320px;
  object-fit: cover;
}

.info-card {
  margin: 12px;
  padding: 16px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
}

.price-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
}

.left-price {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 4px;
}

.currency {
  font-size: 14px;
  color: #ee0a24;
  font-weight: 700;
}

.sale-price {
  font-size: 30px;
  line-height: 1;
  color: #ee0a24;
  font-weight: 700;
}

.market-price {
  font-size: 13px;
  color: #a0a8b0;
  text-decoration: line-through;
}

.sales-text {
  font-size: 12px;
  color: #7b8794;
}

.product-name {
  margin-top: 14px;
  font-size: 19px;
  line-height: 1.5;
  font-weight: 700;
  color: #1f2d3d;
}

.product-subtitle {
  margin-top: 8px;
  font-size: 13px;
  line-height: 1.7;
  color: #7f8b96;
}

.tag-row {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 5px 10px;
  border-radius: 999px;
  background: #f5f8fb;
  color: #66707a;
  font-size: 12px;
}

.tag--recommend {
  background: #fff1eb;
  color: #ff6b3d;
}

.detail-card {
  margin: 12px;
  padding: 16px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2d3d;
  margin-bottom: 14px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  font-size: 13px;
  line-height: 1.6;
}

.label {
  min-width: 68px;
  color: #8a96a3;
}

.value {
  flex: 1;
  text-align: right;
  color: #1f2d3d;
  word-break: break-all;
}

.description-content {
  font-size: 14px;
  line-height: 1.8;
  color: #36404a;
  white-space: pre-wrap;
  word-break: break-word;
}

.bottom-safe-space {
  height: 82px;
}

.bottom-action {
  position: fixed;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  width: 100%;
  max-width: 420px;
  height: 62px;
  padding: 8px 12px calc(8px + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, 0.98);
  display: flex;
  align-items: center;
  gap: 8px;
  border-top: 1px solid #edf1f5;
  box-sizing: border-box;
}

.action-left {
  width: 52px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  color: #687684;
  font-size: 11px;
}

.cart-btn {
  flex: 1;
  height: 40px;
}

.buy-btn {
  flex: 1.2;
  height: 40px;
}
</style>