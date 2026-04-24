<template>
  <div class="page">
    <div class="mobile-shell">
      <div class="top-bar">
        <van-icon name="arrow-left" size="20" @click="goBack" />
        <span class="top-title">提交订单</span>
        <span class="top-placeholder"></span>
      </div>

      <div v-if="loading" class="loading-wrap">
        <van-loading size="24px" vertical>加载中...</van-loading>
      </div>

      <template v-else>
        <van-empty
          v-if="checkedItems.length === 0"
          image="cart-o"
          description="当前没有勾选的商品，无法提交订单"
        >
          <van-button round type="primary" @click="goCart">返回购物车</van-button>
        </van-empty>

        <template v-else>
          <div class="card">
            <div class="section-header">
              <div class="section-title">收货信息</div>
              <span class="action-link" @click="goAddress">去修改</span>
            </div>

            <div v-if="hasShippingInfo" class="shipping-tip">
              已自动带入默认收货信息，可直接提交订单
            </div>

            <van-cell-group inset class="form-group">
              <van-field
                v-model="form.receiver_name"
                label="收货人"
                placeholder="请输入收货人姓名"
                clearable
              />
              <van-field
                v-model="form.receiver_phone"
                label="手机号"
                placeholder="请输入收货手机号"
                clearable
                type="tel"
              />
              <van-field
                v-model="form.receiver_address"
                label="收货地址"
                placeholder="请输入详细收货地址"
                clearable
              />
              <van-field
                v-model="form.remark"
                label="备注"
                placeholder="选填，如配送时间等"
                clearable
              />
            </van-cell-group>
          </div>

          <div class="card">
            <div class="section-title">商品清单</div>

            <div class="order-item-list">
              <div
                v-for="item in checkedItems"
                :key="item.id"
                class="order-item"
              >
                <div class="image-wrap">
                  <img
                    :src="item.product.main_image || defaultImage"
                    :alt="item.product.name"
                    class="product-image"
                  />
                </div>

                <div class="item-info">
                  <div class="product-name van-multi-ellipsis--l2">
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

                    <div class="quantity-text">x{{ item.quantity }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card summary-card">
            <div class="summary-row">
              <span>商品件数</span>
              <span>{{ checkedCount }} 件</span>
            </div>
            <div class="summary-row">
              <span>商品总额</span>
              <span>¥{{ formatPrice(checkedAmount) }}</span>
            </div>
            <div class="summary-row total-row">
              <span>应付金额</span>
              <span class="total-price">¥{{ formatPrice(checkedAmount) }}</span>
            </div>
          </div>

          <div class="bottom-safe-space"></div>

          <van-submit-bar
            :price="submitPrice"
            button-text="提交订单"
            @submit="handleSubmitOrder"
          >
            <template #tip>
              共 {{ checkedCount }} 件商品，提交后会生成待支付订单
            </template>
          </van-submit-bar>
        </template>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  closeToast,
  showConfirmDialog,
  showFailToast,
  showLoadingToast,
  showSuccessToast,
} from 'vant'
import { getCartDetailApi, type CartDetailData, type CartItem } from '@/api/cart'
import { createOrderApi } from '@/api/order'
import { getShippingInfoApi } from '@/api/profile'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(false)
const submitting = ref(false)
const cartData = ref<CartDetailData | null>(null)
const hasShippingInfo = ref(false)

const defaultImage = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

const form = reactive({
  receiver_name: '',
  receiver_phone: '',
  receiver_address: '',
  remark: '',
})

const checkedItems = computed<CartItem[]>(() => {
  return (cartData.value?.items || []).filter((item) => item.checked)
})

const checkedCount = computed(() => {
  return checkedItems.value.reduce((sum, item) => sum + item.quantity, 0)
})

const checkedAmount = computed(() => {
  return checkedItems.value.reduce((sum, item) => {
    return sum + Number(item.product.price) * item.quantity
  }, 0)
})

const submitPrice = computed(() => Math.round(checkedAmount.value * 100))

function formatPrice(value: string | number) {
  return Number(value || 0).toFixed(2)
}

function goBack() {
  router.back()
}

function goCart() {
  router.push('/cart')
}

function goAddress() {
  router.push('/profile/address')
}

async function fetchCartDetail() {
  const res = await getCartDetailApi()
  cartData.value = res.data
  cartStore.setCartCount(res.data.total_count || 0)
}

async function fetchShippingInfo() {
  try {
    const res = await getShippingInfoApi()
    const data = res.data

    form.receiver_name = data.receiver_name || ''
    form.receiver_phone = data.receiver_phone || ''
    form.receiver_address = data.receiver_address || ''

    hasShippingInfo.value = !!(
      form.receiver_name.trim() &&
      form.receiver_phone.trim() &&
      form.receiver_address.trim()
    )
  } catch (error: any) {
    hasShippingInfo.value = false
  }
}

function validateForm() {
  if (!form.receiver_name.trim()) {
    showFailToast('请输入收货人姓名')
    return false
  }

  if (!form.receiver_phone.trim()) {
    showFailToast('请输入收货手机号')
    return false
  }

  if (!/^1\d{10}$/.test(form.receiver_phone.trim())) {
    showFailToast('请输入正确的手机号')
    return false
  }

  if (!form.receiver_address.trim()) {
    showFailToast('请输入收货地址')
    return false
  }

  if (checkedItems.value.length === 0) {
    showFailToast('当前没有勾选的商品')
    return false
  }

  return true
}

async function handleSubmitOrder() {
  if (submitting.value) return
  if (!validateForm()) return

  try {
    await showConfirmDialog({
      title: '确认提交',
      message: '确定提交当前订单吗？',
    })

    submitting.value = true

    showLoadingToast({
      message: '正在提交订单...',
      forbidClick: true,
      duration: 0,
    })

    const res = await createOrderApi({
      receiver_name: form.receiver_name.trim(),
      receiver_phone: form.receiver_phone.trim(),
      receiver_address: form.receiver_address.trim(),
      remark: form.remark.trim(),
    })

    await fetchCartDetail()

    closeToast()
    showSuccessToast(`订单创建成功：${res.data.order_no}`)

    setTimeout(() => {
      router.replace('/')
    }, 800)
  } catch (error: any) {
    closeToast()

    if (error === 'cancel') return

    showFailToast(
      error?.response?.data?.message ||
      error?.response?.data?.detail ||
      '提交订单失败',
    )
  } finally {
    submitting.value = false
  }
}

async function initPage() {
  try {
    loading.value = true
    await Promise.all([fetchCartDetail(), fetchShippingInfo()])
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
      error?.response?.data?.detail ||
      '页面初始化失败',
    )
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  initPage()
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

.top-placeholder {
  width: 20px;
}

.loading-wrap {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  margin: 12px;
  padding: 14px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2d3d;
  margin-bottom: 12px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.action-link {
  font-size: 13px;
  color: #1989fa;
}

.shipping-tip {
  margin-bottom: 12px;
  padding: 10px 12px;
  border-radius: 12px;
  background: #edf6ff;
  color: #1989fa;
  font-size: 12px;
  line-height: 1.6;
}

.form-group :deep(.van-cell) {
  padding-left: 0;
  padding-right: 0;
}

.order-item-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  display: flex;
  gap: 10px;
}

.image-wrap {
  width: 88px;
  min-width: 88px;
  height: 88px;
  border-radius: 14px;
  overflow: hidden;
  background: #f3f5f7;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-info {
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

.quantity-text {
  font-size: 13px;
  color: #36404a;
}

.summary-card {
  padding-top: 8px;
  padding-bottom: 8px;
}

.summary-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  font-size: 14px;
  color: #4b5563;
  border-bottom: 1px solid #f1f4f7;
}

.summary-row:last-child {
  border-bottom: none;
}

.total-row {
  font-weight: 700;
  color: #1f2d3d;
}

.total-price {
  color: #ee0a24;
  font-size: 18px;
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
  background: rgba(255, 255, 255, 0.98);
  border-top: 1px solid #edf1f5;
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