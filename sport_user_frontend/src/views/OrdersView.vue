<template>
  <div class="page">
    <div class="mobile-shell">
      <div class="top-bar">
        <van-icon name="arrow-left" size="20" @click="goBack" />
        <span class="top-title">我的订单</span>
        <span class="top-placeholder"></span>
      </div>

      <div class="tab-wrap">
        <van-tabs v-model:active="activeTab" shrink sticky>
          <van-tab title="全部" name="all" />
          <van-tab title="待支付" name="pending_payment" />
          <van-tab title="已支付" name="paid" />
          <van-tab title="已发货" name="shipped" />
          <van-tab title="已完成" name="completed" />
          <van-tab title="已取消" name="canceled" />
          <van-tab title="已退款" name="refunded" />
        </van-tabs>
      </div>

      <div v-if="loading" class="loading-wrap">
        <van-loading size="24px" vertical>加载中...</van-loading>
      </div>

      <van-empty
        v-else-if="filteredOrders.length === 0"
        image="orders-o"
        description="暂无订单"
      >
        <van-button round type="primary" @click="goHome">去逛逛</van-button>
      </van-empty>

      <div v-else class="order-list">
        <div
          v-for="order in filteredOrders"
          :key="order.id"
          class="order-card"
        >
          <div class="order-header">
            <span class="order-no">订单号：{{ order.order_no }}</span>
            <span :class="['order-status', `status-${order.status}`]">
              {{ formatStatus(order.status) }}
            </span>
          </div>

          <div class="order-body">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="order-item"
            >
              <div class="image-wrap">
                <img
                  :src="item.product_image || defaultImage"
                  :alt="item.product_name"
                  class="product-image"
                />
              </div>

              <div class="item-info">
                <div class="product-name van-multi-ellipsis--l2">
                  {{ item.product_name }}
                </div>

                <div class="item-meta">
                  <span>¥{{ formatPrice(item.product_price) }}</span>
                  <span>x{{ item.quantity }}</span>
                </div>
              </div>
            </div>
          </div>

          <div
            v-if="order.status === 'shipped' || order.status === 'completed'"
            class="shipping-box"
          >
            <div class="shipping-line">
              <span class="shipping-label">物流公司：</span>
              <span class="shipping-value">{{ order.shipping_company || '-' }}</span>
            </div>
            <div class="shipping-line">
              <span class="shipping-label">快递单号：</span>
              <span class="shipping-value">{{ order.tracking_no || '-' }}</span>
            </div>
            <div v-if="order.shipping_remark" class="shipping-line">
              <span class="shipping-label">物流备注：</span>
              <span class="shipping-value">{{ order.shipping_remark }}</span>
            </div>
          </div>

          <div class="order-footer">
            <div class="summary-text">
              共 {{ getOrderItemCount(order) }} 件商品，合计
              <span class="price-text">¥{{ formatPrice(order.total_amount) }}</span>
            </div>

            <div class="time-text">
              {{ formatDateTime(order.created_at) }}
            </div>
          </div>

          <div class="order-actions">
            <template v-if="order.status === 'pending_payment'">
              <van-button size="small" plain round @click="handleCancel(order)">
                取消订单
              </van-button>
              <van-button size="small" type="primary" round @click="handlePay(order)">
                去支付
              </van-button>
            </template>

            <template v-else-if="order.status === 'shipped'">
              <van-button size="small" plain round @click="handleBuyAgain(order)">
                再次购买
              </van-button>
              <van-button size="small" type="primary" round @click="handleComplete(order)">
                确认收货
              </van-button>
            </template>

            <template v-else-if="order.status === 'completed'">
              <van-button size="small" type="primary" round @click="handleBuyAgain(order)">
                再次购买
              </van-button>
            </template>

            <template v-else-if="order.status === 'canceled'">
              <van-button size="small" type="primary" round @click="handleBuyAgain(order)">
                重新下单
              </van-button>
            </template>

            <template v-else-if="order.status === 'paid'">
              <van-button size="small" plain round @click="fetchOrderList">
                刷新状态
              </van-button>
            </template>

            <template v-else-if="order.status === 'refunded'">
              <van-button size="small" plain round @click="handleBuyAgain(order)">
                再次购买
              </van-button>
            </template>
          </div>
        </div>
      </div>

      <div class="bottom-safe-space"></div>
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
  getOrderListApi,
  payOrderApi,
  cancelOrderApi,
  completeOrderApi,
  type OrderDetail,
} from '@/api/order'
import { addCartItemApi } from '@/api/cart'

const router = useRouter()

const loading = ref(false)
const activeTab = ref('all')
const orderList = ref<OrderDetail[]>([])

const defaultImage = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

const filteredOrders = computed(() => {
  if (activeTab.value === 'all') {
    return orderList.value
  }
  return orderList.value.filter((item) => item.status === activeTab.value)
})

function goBack() {
  router.back()
}

function goHome() {
  router.push('/')
}

function formatPrice(value: string | number) {
  return Number(value || 0).toFixed(2)
}

function formatStatus(status: string) {
  const map: Record<string, string> = {
    pending_payment: '待支付',
    paid: '已支付',
    shipped: '已发货',
    completed: '已完成',
    canceled: '已取消',
    refunded: '已退款',
  }
  return map[status] || status || '未知状态'
}

function getOrderItemCount(order: OrderDetail) {
  return order.items.reduce((sum, item) => sum + item.quantity, 0)
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

async function fetchOrderList() {
  try {
    loading.value = true
    const res = await getOrderListApi()
    orderList.value = res.data || []
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '获取订单列表失败',
    )
  } finally {
    loading.value = false
  }
}

async function handlePay(order: OrderDetail) {
  try {
    await showConfirmDialog({
      title: '模拟支付',
      message: `确认支付订单 ${order.order_no} 吗？`,
    })

    await payOrderApi(order.id, { method: 'mock' })
    showSuccessToast('支付成功')
    await fetchOrderList()
  } catch (error: any) {
    if (error === 'cancel') return

    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '支付失败',
    )
  }
}

async function handleCancel(order: OrderDetail) {
  try {
    await showConfirmDialog({
      title: '取消订单',
      message: `确认取消订单 ${order.order_no} 吗？`,
    })

    await cancelOrderApi(order.id, {
      remark: '用户主动取消订单',
    })

    showSuccessToast('订单已取消')
    await fetchOrderList()
  } catch (error: any) {
    if (error === 'cancel') return

    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '取消订单失败',
    )
  }
}

async function handleComplete(order: OrderDetail) {
  try {
    await showConfirmDialog({
      title: '确认收货',
      message: `确认已收到订单 ${order.order_no} 吗？`,
    })

    await completeOrderApi(order.id, {
      remark: '用户确认收货',
    })

    showSuccessToast('已确认收货')
    await fetchOrderList()
  } catch (error: any) {
    if (error === 'cancel') return

    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '确认收货失败',
    )
  }
}

async function handleBuyAgain(order: OrderDetail) {
  try {
    const validItems = order.items.filter((item) => item.product)

    if (validItems.length === 0) {
      showFailToast('该订单没有可重新购买的商品')
      return
    }

    showLoadingToast({
      message: '正在加入购物车...',
      forbidClick: true,
      duration: 0,
    })

    await Promise.all(
      validItems.map((item) =>
        addCartItemApi({
          product_id: Number(item.product),
          quantity: item.quantity,
        }),
      ),
    )

    closeToast()
    showSuccessToast('已加入购物车')
    router.push('/cart')
  } catch (error: any) {
    closeToast()
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '再次购买失败',
    )
  }
}

onMounted(() => {
  fetchOrderList()
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
  z-index: 30;
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

.tab-wrap {
  position: sticky;
  top: 46px;
  z-index: 20;
  background: #fff;
  border-bottom: 1px solid #edf1f5;
}

.loading-wrap {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.order-list {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-card {
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
  overflow: hidden;
}

.order-header {
  padding: 14px 14px 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: #6b7a8c;
  border-bottom: 1px solid #f3f5f7;
}

.order-no {
  flex: 1;
  margin-right: 10px;
  word-break: break-all;
}

.order-status {
  flex-shrink: 0;
  font-weight: 700;
}

.status-pending_payment {
  color: #ff9800;
}

.status-paid {
  color: #1989fa;
}

.status-shipped {
  color: #7c4dff;
}

.status-completed {
  color: #07c160;
}

.status-canceled,
.status-refunded {
  color: #909399;
}

.order-body {
  padding: 0 14px;
}

.order-item {
  padding: 14px 0;
  display: flex;
  gap: 12px;
}

.order-item + .order-item {
  border-top: 1px solid #f5f7fa;
}

.image-wrap {
  width: 76px;
  height: 76px;
  border-radius: 12px;
  overflow: hidden;
  background: #f3f5f7;
  flex-shrink: 0;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.item-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-name {
  font-size: 15px;
  font-weight: 600;
  color: #1f2d3d;
  line-height: 1.45;
}

.item-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #6b7a8c;
  font-size: 14px;
}

.shipping-box {
  margin: 0 14px 10px;
  padding: 10px 12px;
  border-radius: 12px;
  background: #f7f9fc;
  border: 1px dashed #d9e2ec;
}

.shipping-line {
  display: flex;
  font-size: 12px;
  line-height: 1.8;
  color: #4a5568;
}

.shipping-label {
  width: 64px;
  color: #7b8794;
  flex-shrink: 0;
}

.shipping-value {
  flex: 1;
  word-break: break-all;
}

.order-footer {
  padding: 10px 14px 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: flex-end;
  border-top: 1px solid #f5f7fa;
}

.summary-text {
  font-size: 14px;
  color: #4a5568;
}

.price-text {
  color: #ff4d4f;
  font-size: 15px;
  font-weight: 700;
}

.time-text {
  font-size: 12px;
  color: #98a2b3;
}

.order-actions {
  padding: 0 14px 14px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}

.bottom-safe-space {
  height: 24px;
}
</style>