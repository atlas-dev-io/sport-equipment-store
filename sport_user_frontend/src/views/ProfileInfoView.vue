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

      <div class="section-card">
        <div class="section-title">账户服务</div>

        <van-cell-group inset>
          <van-cell
            title="我的订单"
            label="查看全部订单、待支付、已完成等"
            is-link
            @click="goOrders"
          />
          <van-cell
            title="购物车"
            label="查看已加入购物车的商品"
            is-link
            @click="goCart"
          />
          <van-cell
            title="我的收藏"
            label="查看已收藏的商品"
            is-link
            @click="goFavorites"
          />
          <van-cell
            title="浏览记录"
            label="查看近期浏览过的商品"
            is-link
            @click="goHistory"
          />
          <van-cell
            title="猜你喜欢"
            label="规则版推荐 MVP"
            is-link
            @click="goRecommend"
          />
          <van-cell
            title="收货信息"
            label="默认收货信息维护"
            is-link
            @click="showAddressTip"
          />
          <van-cell
            title="个人资料"
            label="昵称、头像、手机号等"
            is-link
            @click="showInfoTip"
          />
        </van-cell-group>
      </div>

      <div class="section-card">
        <div class="section-title">账户操作</div>

        <van-cell-group inset>
          <van-cell
            title="返回首页"
            is-link
            @click="goHome"
          />
          <van-cell
            title="退出登录"
            is-link
            @click="handleLogoutClick"
          />
        </van-cell-group>
      </div>

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
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  showConfirmDialog,
  showFailToast,
  showLoadingToast,
  showSuccessToast,
  closeToast,
} from 'vant'
import { getCurrentUserApi, handleLogout } from '@/api/auth'
import { useUserStore, type CurrentUser } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const userInfo = ref<CurrentUser | null>(userStore.currentUser || null)

const defaultAvatar =
  'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

const avatarUrl = computed(() => {
  return userInfo.value?.avatar || defaultAvatar
})

const displayName = computed(() => {
  return userInfo.value?.nickname || userInfo.value?.username || '未登录用户'
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

function showAddressTip() {
  router.push('/profile/address')
}

function showInfoTip() {
  router.push('/profile/info')
}

async function refreshProfile() {
  try {
    loading.value = true
    const res = await getCurrentUserApi()
    userInfo.value = res.data
    userStore.setCurrentUser(res.data)
    showSuccessToast('刷新成功')
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
  refreshProfile()
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

.section-card {
  margin: 12px;
  padding: 14px 0 4px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
}

.section-title {
  padding: 0 14px;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: 700;
  color: #1f2d3d;
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