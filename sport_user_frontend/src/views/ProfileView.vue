<template>
  <div class="page">
    <div class="mobile-shell">
      <div class="profile-header">
        <div class="header-top">
          <div class="title">我的</div>
          <van-button
            size="small"
            round
            plain
            type="primary"
            @click="refreshProfile"
          >
            刷新
          </van-button>
        </div>

        <div class="user-card">
          <div class="avatar-wrap">
            <img :src="avatarUrl" alt="avatar" class="avatar" />
          </div>

          <div class="user-info">
            <div class="nickname">
              {{ displayName }}
            </div>
            <div class="username">
              用户名：{{ userInfo?.username || '-' }}
            </div>
            <div class="phone">
              手机号：{{ userInfo?.phone || '未绑定' }}
            </div>
            <div class="role-tag">
              {{ formatRole(userInfo?.role) }}
            </div>
          </div>
        </div>
      </div>

      <div class="quick-card">
        <div class="quick-grid">
          <div class="quick-item" @click="goOrders">
            <van-icon name="orders-o" size="22" />
            <span>我的订单</span>
          </div>

          <div class="quick-item" @click="goCart">
            <van-icon name="shopping-cart-o" size="22" />
            <span>购物车</span>
          </div>

          <div class="quick-item" @click="goFavorites">
            <van-icon name="star-o" size="22" />
            <span>我的收藏</span>
          </div>

          <div class="quick-item" @click="goHistory">
            <van-icon name="underway-o" size="22" />
            <span>浏览记录</span>
          </div>

          <div class="quick-item" @click="goRecommend">
            <van-icon name="fire-o" size="22" />
            <span>猜你喜欢</span>
          </div>

          <div class="quick-item" @click="showInfoTip">
            <van-icon name="contact-o" size="22" />
            <span>个人资料</span>
          </div>
        </div>
      </div>

      <div v-if="applicationHintText" class="application-hint">
        {{ applicationHintText }}
      </div>

      <div class="action-buttons">
        <van-button
          v-if="showApplyButton"
          block
          round
          type="primary"
          class="merchant-btn"
          @click="openApplyPopup"
        >
          {{ applyButtonText }}
        </van-button>

        <van-button
          v-if="showPendingButton"
          block
          round
          disabled
          class="merchant-btn"
        >
          商家申请审核中
        </van-button>

        <van-button
          v-if="showAdminEntry"
          block
          round
          plain
          type="primary"
          class="merchant-btn"
          @click="goAdminPanel"
        >
          前往管理端
        </van-button>

        <van-button
          block
          round
          type="danger"
          class="logout-btn"
          @click="handleLogoutClick"
        >
          退出登录
        </van-button>
      </div>

      <van-popup
        v-model:show="showApplyPopup"
        round
        class="merchant-popup"
        closeable
        close-icon-position="top-right"
      >
        <div class="popup-wrap">
          <div class="popup-title">提交商家申请</div>

          <div class="popup-body">
            <van-form @submit="handleSubmitApplication">
              <van-cell-group inset class="popup-group">
                <van-field
                  v-model="applicationForm.shop_name"
                  name="shop_name"
                  label="店铺名称"
                  placeholder="请输入店铺名称"
                  required
                />
                <van-field
                  v-model="applicationForm.contact_name"
                  name="contact_name"
                  label="联系人"
                  placeholder="请输入联系人姓名"
                  required
                />
                <van-field
                  v-model="applicationForm.contact_phone"
                  name="contact_phone"
                  label="联系电话"
                  placeholder="请输入联系电话"
                  required
                />
                <van-field
                  v-model="applicationForm.application_reason"
                  name="application_reason"
                  label="申请说明"
                  type="textarea"
                  rows="4"
                  autosize
                  placeholder="可填写主营商品、经营说明等"
                />
              </van-cell-group>

              <div class="popup-btns">
                <van-button round block plain @click="showApplyPopup = false">
                  取消
                </van-button>
                <van-button
                  round
                  block
                  type="primary"
                  native-type="submit"
                  :loading="submittingApplication"
                >
                  提交申请
                </van-button>
              </div>
            </van-form>
          </div>
        </div>
      </van-popup>

      <div class="bottom-safe-space"></div>

      <div class="bottom-tabbar">
        <div class="tab-item" @click="goHome">
          <van-icon name="home-o" size="20" />
          <span>首页</span>
        </div>

        <div class="tab-item" @click="goCart">
          <van-icon name="shopping-cart-o" size="20" />
          <span>购物车</span>
        </div>

        <div class="tab-item tab-item--active" @click="goProfile">
          <van-icon name="contact-o" size="20" />
          <span>我的</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  showConfirmDialog,
  showFailToast,
  showLoadingToast,
  showSuccessToast,
  closeToast,
} from 'vant'
import {
  becomeMerchantApi,
  getCurrentUserApi,
  handleLogout,
} from '@/api/auth'
import { useUserStore, type CurrentUser } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const submittingApplication = ref(false)
const showApplyPopup = ref(false)
const userInfo = ref<CurrentUser | null>(userStore.currentUser || null)

const applicationForm = reactive({
  shop_name: '',
  contact_name: '',
  contact_phone: '',
  application_reason: '',
})

const defaultAvatar =
  'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

const avatarUrl = computed(() => {
  return userInfo.value?.avatar || defaultAvatar
})

const displayName = computed(() => {
  return userInfo.value?.nickname || userInfo.value?.username || '未登录用户'
})

const applicationStatus = computed(() => {
  return userInfo.value?.merchant_application_status || ''
})

const showApplyButton = computed(() => {
  const role = userInfo.value?.role || 'customer'
  return role === 'customer' && applicationStatus.value !== 'pending'
})

const showPendingButton = computed(() => {
  const role = userInfo.value?.role || 'customer'
  return role === 'customer' && applicationStatus.value === 'pending'
})

const showAdminEntry = computed(() => {
  const role = userInfo.value?.role || 'customer'
  return role === 'merchant' || role === 'admin'
})

const applyButtonText = computed(() => {
  if (applicationStatus.value === 'rejected') {
    return '重新申请成为商家'
  }
  return '申请成为商家'
})

const applicationHintText = computed(() => {
  if (applicationStatus.value === 'pending') {
    const shopName = userInfo.value?.merchant_application_shop_name || ''
    return shopName
      ? `你的商家申请（${shopName}）正在审核中，请耐心等待。`
      : '你的商家申请正在审核中，请耐心等待。'
  }

  if (applicationStatus.value === 'rejected') {
    const reason = userInfo.value?.merchant_application_review_remark || '暂无审核备注'
    return `你的商家申请未通过，原因：${reason}`
  }

  if ((userInfo.value?.role || '') === 'merchant') {
    return '你的商家身份已开通，可前往管理端进行商品、订单和库存管理。'
  }

  return ''
})

function formatRole(role?: string) {
  const roleMap: Record<string, string> = {
    customer: '普通用户',
    merchant: '商家',
    admin: '管理员',
  }
  return roleMap[role || ''] || '普通用户'
}

function goHome() {
  router.push('/')
}

function goCart() {
  router.push('/cart')
}

function goOrders() {
  router.push('/orders')
}

function goFavorites() {
  router.push('/profile/favorites')
}

function goHistory() {
  router.push('/profile/history')
}

function goRecommend() {
  router.push('/profile/recommend')
}

function goProfile() {
  router.push('/profile')
}

function showInfoTip() {
  router.push('/profile/info')
}

function goAdminPanel() {
  const adminUrl =
    (import.meta.env.VITE_ADMIN_URL as string) || 'http://localhost:5174/login'
  window.location.href = adminUrl
}

function resetApplicationForm() {
  applicationForm.shop_name = ''
  applicationForm.contact_name = userInfo.value?.nickname || ''
  applicationForm.contact_phone = userInfo.value?.phone || ''
  applicationForm.application_reason = ''
}

function openApplyPopup() {
  resetApplicationForm()
  showApplyPopup.value = true
}

async function refreshProfile(showToast = true) {
  try {
    loading.value = true
    const res = await getCurrentUserApi()
    userInfo.value = res.data
    userStore.setCurrentUser(res.data)
    if (showToast) {
      showSuccessToast('刷新成功')
    }
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '获取个人信息失败',
    )
  } finally {
    loading.value = false
  }
}

async function handleSubmitApplication() {
  if (!applicationForm.shop_name.trim()) {
    showFailToast('请输入店铺名称')
    return
  }
  if (!applicationForm.contact_name.trim()) {
    showFailToast('请输入联系人')
    return
  }
  if (!applicationForm.contact_phone.trim()) {
    showFailToast('请输入联系电话')
    return
  }

  try {
    submittingApplication.value = true

    showLoadingToast({
      message: '正在提交申请...',
      forbidClick: true,
      duration: 0,
    })

    await becomeMerchantApi({
      shop_name: applicationForm.shop_name.trim(),
      contact_name: applicationForm.contact_name.trim(),
      contact_phone: applicationForm.contact_phone.trim(),
      application_reason: applicationForm.application_reason.trim(),
    })

    closeToast()
    showApplyPopup.value = false
    showSuccessToast('商家申请已提交')

    await refreshProfile(false)
  } catch (error: any) {
    closeToast()
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '提交申请失败',
    )
  } finally {
    submittingApplication.value = false
  }
}

async function handleLogoutClick() {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定要退出登录吗？',
    })

    showLoadingToast({
      message: '正在退出...',
      forbidClick: true,
      duration: 0,
    })

    await handleLogout()

    closeToast()
    showSuccessToast('已退出登录')

    setTimeout(() => {
      router.replace('/login')
    }, 500)
  } catch (error: any) {
    closeToast()

    if (error === 'cancel') return

    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '退出登录失败',
    )
  }
}

onMounted(() => {
  refreshProfile(false)
  resetApplicationForm()
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

.profile-header {
  padding: 16px 14px 18px;
  background: linear-gradient(180deg, #eaf4ff 0%, #f8fbff 100%);
  border-bottom: 1px solid #edf1f5;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2d3d;
}

.user-card {
  display: flex;
  gap: 14px;
  padding: 16px;
  border-radius: 20px;
  background: #ffffff;
  box-shadow: 0 6px 16px rgba(31, 45, 61, 0.06);
}

.avatar-wrap {
  width: 72px;
  min-width: 72px;
  height: 72px;
  border-radius: 50%;
  overflow: hidden;
  background: #f3f5f7;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.nickname {
  font-size: 20px;
  font-weight: 700;
  color: #1f2d3d;
  line-height: 1.4;
}

.username,
.phone {
  margin-top: 6px;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.6;
}

.role-tag {
  display: inline-block;
  margin-top: 10px;
  padding: 5px 10px;
  border-radius: 999px;
  background: #edf6ff;
  color: #1989fa;
  font-size: 12px;
}

.quick-card {
  margin: 12px;
  padding: 14px 10px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.quick-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 6px;
  color: #4b5563;
  font-size: 12px;
  text-align: center;
}

.application-hint {
  margin: 0 12px 12px;
  padding: 12px 14px;
  border-radius: 14px;
  background: #fff7e6;
  color: #ad6800;
  font-size: 13px;
  line-height: 1.7;
}

.action-buttons {
  margin: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.merchant-btn,
.logout-btn {
  height: 44px;
}

.merchant-popup {
  width: calc(100% - 32px);
  max-width: 372px;
  max-height: 76vh;
  overflow: hidden;
  border-radius: 20px;
  background: #fff;
}

.popup-wrap {
  display: flex;
  flex-direction: column;
  max-height: 76vh;
}

.popup-title {
  flex-shrink: 0;
  padding: 18px 44px 14px 44px;
  font-size: 18px;
  font-weight: 700;
  color: #1f2d3d;
  text-align: center;
  border-bottom: 1px solid #f2f4f7;
}

.popup-body {
  flex: 1;
  overflow-y: auto;
  padding: 14px 0 18px;
}

.popup-group {
  margin: 0 12px;
}

.popup-btns {
  padding: 18px 16px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.popup-btns :deep(.van-button) {
  height: 44px;
}

.merchant-popup :deep(.van-field__label) {
  width: 72px;
  flex: none;
}

.merchant-popup :deep(.van-cell) {
  align-items: flex-start;
}

.merchant-popup :deep(.van-field__control) {
  line-height: 1.5;
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