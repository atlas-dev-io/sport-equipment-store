<template>
  <div class="page">
    <div class="mobile-shell">
      <div class="page-header">
        <div class="header-top">
          <div>
            <div class="page-title">运动装备商城</div>
            <div class="page-subtitle">精选商品，随时下单</div>
          </div>

          <van-button size="small" round plain type="primary" @click="goLogin">
            {{ isLogin ? '我的' : '登录' }}
          </van-button>
        </div>

        <van-search
          v-model="keyword"
          shape="round"
          placeholder="搜索商品名称 / 品牌 / SKU"
          @search="onSearch"
          @clear="onSearch"
        />

        <div class="toolbar-row">
          <div class="sort-group">
            <span
              v-for="item in sortOptions"
              :key="item.value"
              :class="['sort-chip', activeOrdering === item.value ? 'sort-chip--active' : '']"
              @click="changeOrdering(item.value)"
            >
              {{ item.label }}
            </span>
          </div>

          <span
            :class="['recommend-chip', recommendOnly ? 'recommend-chip--active' : '']"
            @click="toggleRecommend"
          >
            推荐商品
          </span>
        </div>
      </div>

      <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
        <div class="content-area">
          <div
            v-if="isLogin && recommendList.length > 0"
            class="section-card"
          >
            <div class="section-head">
              <div>
                <div class="section-title">猜你喜欢</div>
                <div class="section-subtitle">基于浏览记录、收藏偏好与热门商品</div>
              </div>
              <span class="section-link" @click="goRecommend">查看更多</span>
            </div>

            <div class="mini-horizontal-list">
              <div
                v-for="item in recommendList"
                :key="item.product.id"
                class="mini-product-card"
                @click="goDetail(item.product.id)"
              >
                <div class="mini-image-wrap">
                  <img
                    :src="item.product.main_image || defaultImage"
                    :alt="item.product.name"
                    class="mini-product-image"
                  />
                </div>

                <div class="mini-product-name van-multi-ellipsis--l2">
                  {{ item.product.name }}
                </div>

                <div class="mini-reason van-ellipsis">
                  {{ item.reason || '热门商品兜底' }}
                </div>

                <div class="mini-price-row">
                  <span class="mini-price">¥{{ formatPrice(item.product.price) }}</span>
                  <span class="mini-score">分 {{ item.score }}</span>
                </div>
              </div>
            </div>
          </div>

          <div
            v-if="isLogin && historyList.length > 0"
            class="section-card"
          >
            <div class="section-head">
              <div>
                <div class="section-title">最近浏览</div>
                <div class="section-subtitle">你最近看过的商品会影响推荐结果</div>
              </div>
              <span class="section-link" @click="goHistory">查看更多</span>
            </div>

            <div class="mini-horizontal-list">
              <div
                v-for="item in historyList"
                :key="item.id"
                class="mini-product-card"
                @click="goDetail(item.product.id)"
              >
                <div class="mini-image-wrap">
                  <img
                    :src="item.product.main_image || defaultImage"
                    :alt="item.product.name"
                    class="mini-product-image"
                  />
                </div>

                <div class="mini-product-name van-multi-ellipsis--l2">
                  {{ item.product.name }}
                </div>

                <div class="mini-reason van-ellipsis">
                  {{ item.product.brand || '未标注品牌' }} / {{ item.product.category_name || '未分类' }}
                </div>

                <div class="mini-price-row">
                  <span class="mini-price">¥{{ formatPrice(item.product.price) }}</span>
                </div>
              </div>
            </div>
          </div>

          <van-list
            v-model:loading="loading"
            :finished="finished"
            finished-text="没有更多商品了"
            @load="onLoad"
          >
            <div class="list-title-wrap">
              <div class="list-title">全部商品</div>
              <div class="list-subtitle">
                当前共加载 {{ loadedCount }} / {{ total }} 件
              </div>
            </div>

            <div v-if="productList.length > 0" class="product-list">
              <div
                v-for="item in productList"
                :key="item.id"
                class="product-card"
                @click="goDetail(item.id)"
              >
                <div class="image-wrap">
                  <img
                    :src="item.main_image || defaultImage"
                    :alt="item.name"
                    class="product-image"
                  />
                  <span v-if="item.is_recommend" class="recommend-badge">推荐</span>
                </div>

                <div class="product-info">
                  <div class="product-name van-multi-ellipsis--l2">
                    {{ item.name }}
                  </div>

                  <div v-if="item.subtitle" class="product-subtitle van-ellipsis">
                    {{ item.subtitle }}
                  </div>

                  <div class="meta-row">
                    <span class="brand-text">{{ item.brand || '未标注品牌' }}</span>
                    <span class="category-text">{{ item.category_name || '未分类' }}</span>
                  </div>

                  <div class="sales-row">
                    <span>销量 {{ item.sales_count }}</span>
                    <span>库存 {{ item.stock }}</span>
                  </div>

                  <div class="price-row">
                    <div class="price-block">
                      <span class="currency">¥</span>
                      <span class="sale-price">{{ formatPrice(item.price) }}</span>
                      <span
                        v-if="showMarketPrice(item.market_price, item.price)"
                        class="market-price"
                      >
                        ¥{{ formatPrice(item.market_price) }}
                      </span>
                    </div>

                    <van-button
                      size="small"
                      round
                      type="primary"
                      class="detail-btn"
                      @click.stop="goDetail(item.id)"
                    >
                      查看
                    </van-button>
                  </div>
                </div>
              </div>
            </div>

            <van-empty
              v-else-if="!loading && !refreshing"
              image="search"
              description="暂无商品数据"
            />
          </van-list>
        </div>
      </van-pull-refresh>

      <div class="bottom-safe-space"></div>

      <div class="bottom-tabbar">
        <div class="tab-item tab-item--active" @click="goHome">
          <van-icon name="home-o" size="20" />
          <span>首页</span>
        </div>

        <div class="tab-item" @click="goCart">
          <van-icon name="shopping-cart-o" size="20" />
          <span>购物车</span>
        </div>

        <div class="tab-item" @click="goProfile">
          <van-icon name="contact-o" size="20" />
          <span>我的</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast } from 'vant'
import { getProductListApi, type ProductItem } from '@/api/product'
import {
  getBrowseHistoryListApi,
  getRecommendProductListApi,
  type BrowseHistoryItem,
  type RecommendProductItem,
} from '@/api/recommend'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const defaultImage =
  'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

const keyword = ref('')
const activeOrdering = ref('-id')
const recommendOnly = ref(false)

const productList = ref<ProductItem[]>([])
const recommendList = ref<RecommendProductItem[]>([])
const historyList = ref<BrowseHistoryItem[]>([])

const loading = ref(false)
const refreshing = ref(false)
const finished = ref(false)

const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const isLogin = computed(() => userStore.isLogin)
const loadedCount = computed(() => productList.value.length)

const sortOptions = [
  { label: '最新', value: '-id' },
  { label: '价格↑', value: 'price' },
  { label: '价格↓', value: '-price' },
  { label: '销量↑', value: 'sales_count' },
  { label: '销量↓', value: '-sales_count' },
]

function formatPrice(value: string | number) {
  const num = Number(value || 0)
  return num.toFixed(2)
}

function showMarketPrice(marketPrice: string | number, salePrice: string | number) {
  return Number(marketPrice) > Number(salePrice)
}

function goLogin() {
  if (isLogin.value) {
    router.push('/profile')
    return
  }
  router.push('/login')
}

function goDetail(id: number) {
  router.push(`/product/${id}`)
}

function goRecommend() {
  router.push('/profile/recommend')
}

function goHistory() {
  router.push('/profile/history')
}

async function fetchProductList(reset = false) {
  if (reset) {
    page.value = 1
    total.value = 0
    finished.value = false
    productList.value = []
  }

  try {
    const res = await getProductListApi({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value.trim(),
      is_recommend: recommendOnly.value,
      ordering: activeOrdering.value,
    })

    const list = res?.results?.data ?? []
    total.value = res?.count ?? 0

    if (reset) {
      productList.value = list
    } else {
      productList.value = [...productList.value, ...list]
    }

    const noMoreByCount = productList.value.length >= total.value
    const noMoreByNext = !res?.next
    finished.value = noMoreByCount || noMoreByNext

    if (!finished.value) {
      page.value += 1
    }
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '获取商品列表失败',
    )
    finished.value = true
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

async function fetchRecommendBlocks() {
  if (!isLogin.value) {
    recommendList.value = []
    historyList.value = []
    return
  }

  try {
    const [recommendRes, historyRes] = await Promise.all([
      getRecommendProductListApi(6),
      getBrowseHistoryListApi(),
    ])

    recommendList.value = recommendRes.data || []
    historyList.value = (historyRes.data || []).slice(0, 6)
  } catch (error: any) {
    recommendList.value = []
    historyList.value = []
  }
}

function onLoad() {
  fetchProductList(false)
}

async function onRefresh() {
  await Promise.all([fetchProductList(true), fetchRecommendBlocks()])
}

function onSearch() {
  loading.value = false
  refreshing.value = false
  fetchProductList(true)
}

function changeOrdering(ordering: string) {
  if (activeOrdering.value === ordering) return
  activeOrdering.value = ordering
  onSearch()
}

function toggleRecommend() {
  recommendOnly.value = !recommendOnly.value
  onSearch()
}

function goHome() {
  router.push('/')
}

function goCart() {
  router.push('/cart')
}

function goProfile() {
  router.push('/profile')
}

onMounted(async () => {
  await Promise.all([fetchProductList(true), fetchRecommendBlocks()])
})
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

.page-header {
  position: sticky;
  top: 0;
  z-index: 10;
  padding: 14px 14px 10px;
  background: linear-gradient(180deg, #eaf4ff 0%, #f8fbff 100%);
  border-bottom: 1px solid #edf1f5;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2d3d;
}

.page-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #7b8a97;
}

.toolbar-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  margin-top: 10px;
}

.sort-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.sort-chip,
.recommend-chip {
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 12px;
  line-height: 1;
  background: #ffffff;
  color: #66707a;
  border: 1px solid #e6ebf0;
  transition: all 0.2s ease;
}

.sort-chip--active,
.recommend-chip--active {
  color: #1989fa;
  border-color: #b6d8ff;
  background: #edf6ff;
}

.content-area {
  padding: 12px;
}

.section-card {
  margin-bottom: 12px;
  padding: 14px 12px;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
}

.section-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 12px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2d3d;
}

.section-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #7b8794;
}

.section-link {
  flex-shrink: 0;
  font-size: 12px;
  color: #1989fa;
  line-height: 22px;
}

.mini-horizontal-list {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 2px;
}

.mini-horizontal-list::-webkit-scrollbar {
  display: none;
}

.mini-product-card {
  width: 132px;
  min-width: 132px;
  padding: 10px;
  border-radius: 16px;
  background: #f8fafc;
}

.mini-image-wrap {
  width: 100%;
  height: 112px;
  border-radius: 12px;
  overflow: hidden;
  background: #eef2f6;
}

.mini-product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mini-product-name {
  margin-top: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #1f2d3d;
  line-height: 1.45;
  min-height: 38px;
}

.mini-reason {
  margin-top: 6px;
  font-size: 11px;
  color: #7b8794;
}

.mini-price-row {
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.mini-price {
  color: #ee0a24;
  font-size: 14px;
  font-weight: 700;
}

.mini-score {
  font-size: 11px;
  color: #1989fa;
}

.list-title-wrap {
  margin-bottom: 10px;
  padding: 0 2px;
}

.list-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2d3d;
}

.list-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #7b8794;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-card {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
}

.image-wrap {
  position: relative;
  width: 110px;
  min-width: 110px;
  height: 110px;
  border-radius: 14px;
  overflow: hidden;
  background: #f3f5f7;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.recommend-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 4px 8px;
  border-radius: 999px;
  font-size: 10px;
  color: #fff;
  background: linear-gradient(135deg, #ff8a65 0%, #ff7043 100%);
}

.product-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-size: 15px;
  font-weight: 700;
  color: #1f2d3d;
  line-height: 1.45;
}

.product-subtitle {
  margin-top: 6px;
  font-size: 12px;
  color: #7f8b96;
}

.meta-row,
.sales-row {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  margin-top: 8px;
  font-size: 12px;
  color: #7b8794;
}

.brand-text,
.category-text {
  max-width: 48%;
}

.price-row {
  margin-top: auto;
  padding-top: 10px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 8px;
}

.price-block {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 4px;
}

.currency {
  font-size: 12px;
  color: #ee0a24;
  font-weight: 700;
}

.sale-price {
  font-size: 22px;
  color: #ee0a24;
  font-weight: 700;
  line-height: 1;
}

.market-price {
  font-size: 12px;
  color: #a0a8b0;
  text-decoration: line-through;
}

.detail-btn {
  min-width: 68px;
}

.bottom-safe-space {
  height: 72px;
}

.bottom-tabbar {
  position: fixed;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  width: 100%;
  max-width: 420px;
  height: 62px;
  padding: 8px 0 calc(8px + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, 0.98);
  border-top: 1px solid #edf1f5;
  display: flex;
  align-items: center;
  justify-content: space-around;
  box-sizing: border-box;
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  color: #7b8794;
  font-size: 11px;
}

.tab-item--active {
  color: #1989fa;
}
</style>