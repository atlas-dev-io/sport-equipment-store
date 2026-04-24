<template>
  <div class="page">
    <div class="mobile-shell">
      <div class="top-bar">
        <van-icon name="arrow-left" size="20" @click="goBack" />
        <span class="top-title">购物车</span>
        <span class="clear-btn" @click="handleClearCart">清空</span>
      </div>

      <div v-if="loading" class="loading-wrap">
        <van-loading size="24px" vertical>加载中...</van-loading>
      </div>

      <template v-else>
        <van-empty
          v-if="cartItems.length === 0"
          image="cart-o"
          description="购物车还是空的，快去挑选商品吧"
        >
          <van-button round type="primary" @click="goHome">去逛逛</van-button>
        </van-empty>

        <div v-else class="cart-list">
          <van-swipe-cell v-for="item in cartItems" :key="item.id">
            <div class="cart-card">
              <div class="check-wrap">
                <van-checkbox
                  :model-value="item.checked"
                  checked-color="#1989fa"
                  @update:model-value="(val) => handleToggleChecked(item, val)"
                />
              </div>

              <div class="image-wrap" @click="goDetail(item.product.id)">
                <img
                  :src="item.product.main_image || defaultImage"
                  :alt="item.product.name"
                  class="product-image"
                />
              </div>

              <div class="info-wrap">
                <div class="product-name van-multi-ellipsis--l2" @click="goDetail(item.product.id)">
                  {{ item.product.name }}
                </div>

                <div v-if="item.product.subtitle" class="product-subtitle van-ellipsis">
                  {{ item.product.subtitle }}
                </div>

                <div class="meta-row">
                  <span>{{ item.product.brand || '未标注品牌' }}</span>
                  <span>{{ item.product.category_name || '未分类' }}</span>
                </div>

                <div class="bottom-row">
                  <div class="price-wrap">
                    <span class="currency">¥</span>
                    <span class="sale-price">{{ formatPrice(item.product.price) }}</span>
                  </div>

                  <van-stepper
                    :model-value="item.quantity"
                    min="1"
                    integer
                    button-size="24"
                    theme="round"
                    @update:model-value="(val) => handleQuantityChange(item, Number(val))"
                  />
                </div>
              </div>
            </div>

            <template #right>
              <van-button
                square
                text="删除"
                type="danger"
                class="delete-button"
                @click="handleDeleteItem(item.id)"
              />
            </template>
          </van-swipe-cell>
        </div>
      </template>

      <div class="bottom-safe-space"></div>

      <van-submit-bar
        v-if="cartItems.length > 0"
        :price="submitPrice"
        button-text="去结算"
        @submit="goCheckout"
      >
        <van-checkbox
          :model-value="isAllChecked"
          checked-color="#1989fa"
          @update:model-value="handleToggleAll"
        >
          全选
        </van-checkbox>

        <template #tip>
          已选 {{ checkedCount }} 件商品
        </template>
      </van-submit-bar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  showConfirmDialog,
  showFailToast,
  showLoadingToast,
  showSuccessToast,
  closeToast,
} from 'vant'
import {
  clearCartApi,
  deleteCartItemApi,
  getCartDetailApi,
  updateCartItemApi,
  type CartDetailData,
  type CartItem,
} from '@/api/cart'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(false)
const cartData = ref<CartDetailData | null>(null)

const defaultImage = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

const cartItems = computed(() => cartData.value?.items || [])

const checkedCount = computed(() => cartData.value?.checked_count || 0)

const checkedAmount = computed(() => Number(cartData.value?.checked_amount || 0))

const submitPrice = computed(() => Math.round(checkedAmount.value * 100))

const isAllChecked = computed(() => {
  if (cartItems.value.length === 0) return false
  return cartItems.value.every((item) => item.checked)
})

function formatPrice(value: string | number) {
  return Number(value || 0).toFixed(2)
}

function goBack() {
  router.back()
}

function goHome() {
  router.push('/')
}

function goDetail(id: number) {
  router.push(`/product/${id}`)
}

function goCheckout() {
  if (checkedCount.value <= 0) {
    showFailToast('请先勾选要结算的商品')
    return
  }

  router.push('/checkout')
}

async function fetchCartDetail() {
  try {
    loading.value = true
    const res = await getCartDetailApi()
    cartData.value = res.data
    cartStore.setCartCount(res.data.total_count || 0)
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '获取购物车失败',
    )
  } finally {
    loading.value = false
  }
}

async function handleToggleChecked(item: CartItem, checked: boolean) {
  try {
    await updateCartItemApi(item.id, { checked })
    item.checked = checked
    await fetchCartDetail()
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '更新勾选状态失败',
    )
  }
}

async function handleToggleAll(checked: boolean) {
  try {
    showLoadingToast({
      message: '处理中...',
      forbidClick: true,
      duration: 0,
    })

    await Promise.all(
      cartItems.value.map((item) =>
        updateCartItemApi(item.id, { checked }),
      ),
    )

    await fetchCartDetail()
    showSuccessToast(checked ? '已全选' : '已取消全选')
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '全选操作失败',
    )
  } finally {
    closeToast()
  }
}

async function handleQuantityChange(item: CartItem, value: number) {
  if (!value || value < 1) return

  try {
    await updateCartItemApi(item.id, { quantity: value })
    item.quantity = value
    await fetchCartDetail()
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '更新数量失败',
    )
  }
}

async function handleDeleteItem(id: number) {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定删除这个商品吗？',
    })

    await deleteCartItemApi(id)
    showSuccessToast('删除成功')
    await fetchCartDetail()
  } catch (error: any) {
    if (error === 'cancel') return

    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '删除失败',
    )
  }
}

async function handleClearCart() {
  if (cartItems.value.length === 0) {
    showFailToast('购物车已经是空的了')
    return
  }

  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定清空购物车吗？',
    })

    await clearCartApi()
    showSuccessToast('购物车已清空')
    await fetchCartDetail()
  } catch (error: any) {
    if (error === 'cancel') return

    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '清空购物车失败',
    )
  }
}

onMounted(() => {
  fetchCartDetail()
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

.top-bar {
  position: sticky;
  top: 0;
  z-index: 20;
  height: 46px;
  padding: 0 14px;
  background: rgba(255, 255, 255, 0.96);
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

.clear-btn {
  font-size: 13px;
  color: #1989fa;
}

.loading-wrap {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-list {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cart-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
}

.check-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-wrap {
  width: 92px;
  min-width: 92px;
  height: 92px;
  border-radius: 14px;
  overflow: hidden;
  background: #f3f5f7;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info-wrap {
  flex: 1;
  min-width: 0;
}

.product-name {
  font-size: 15px;
  line-height: 1.45;
  font-weight: 700;
  color: #1f2d3d;
}

.product-subtitle {
  margin-top: 6px;
  font-size: 12px;
  color: #7f8b96;
}

.meta-row {
  margin-top: 8px;
  display: flex;
  justify-content: space-between;
  gap: 8px;
  font-size: 12px;
  color: #7b8794;
}

.bottom-row {
  margin-top: 12px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 8px;
}

.price-wrap {
  display: flex;
  align-items: baseline;
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

.delete-button {
  height: 100%;
}

.bottom-safe-space {
  height: 110px;
}

:deep(.van-submit-bar) {
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 420px;
  box-sizing: border-box;
  padding-bottom: calc(env(safe-area-inset-bottom));
}

:deep(.van-submit-bar__bar) {
  width: 100%;
  max-width: 420px;
  margin: 0 auto;
  box-sizing: border-box;
}

:deep(.van-submit-bar__tip) {
  width: 100%;
  max-width: 420px;
  margin: 0 auto;
  box-sizing: border-box;
}
</style>