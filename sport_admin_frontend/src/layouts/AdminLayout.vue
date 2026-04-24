<template>
  <n-layout has-sider class="admin-layout">
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="220"
      :collapsed="collapsed"
      show-trigger
      @collapse="collapsed = true"
      @expand="collapsed = false"
    >
      <div class="logo-wrap">
        <div class="logo-mark">运</div>
        <span v-show="!collapsed" class="logo-text">运动装备商城管理端</span>
      </div>

      <n-menu
        :collapsed="collapsed"
        :collapsed-width="64"
        :collapsed-icon-size="20"
        :options="menuOptions"
        :value="activeMenu"
        @update:value="handleMenuClick"
      />
    </n-layout-sider>

    <n-layout>
      <n-layout-header bordered class="header">
        <div class="header-left">
          <div class="page-title">{{ currentTitle }}</div>
        </div>

        <div class="header-right">
          <div class="user-panel">
            <div class="user-meta">
              <n-tag class="role-tag" round :bordered="false" type="info" size="small">
                {{ roleText }}
              </n-tag>
              <span class="username">{{ adminUserStore.username }}</span>
            </div>

            <n-button
              secondary
              type="error"
              size="small"
              round
              class="logout-btn"
              @click="handleLogoutClick"
            >
              退出登录
            </n-button>
          </div>
        </div>
      </n-layout-header>

      <n-layout-content content-style="padding: 16px;">
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import { computed, h, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { NIcon, useDialog } from 'naive-ui'
import { useAdminUserStore } from '@/stores/adminUser'
import { adminMenuList } from '@/constants/adminMenu'
import { handleAdminLogout } from '@/api/auth'

const route = useRoute()
const router = useRouter()
const dialog = useDialog()
const adminUserStore = useAdminUserStore()
const collapsed = ref(false)

function renderIcon(icon: any) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions = computed(() => {
  return adminMenuList
    .filter((item) => item.roles.includes(adminUserStore.role as 'merchant' | 'admin'))
    .map((item) => ({
      label: () =>
        h(
          RouterLink,
          { to: item.key },
          { default: () => item.label },
        ),
      key: item.key,
      icon: renderIcon(item.icon),
    }))
})

const activeMenu = computed(() => route.path)

const currentTitle = computed(() => {
  return (route.meta.title as string) || '管理端'
})

const roleText = computed(() => {
  return adminUserStore.role === 'admin' ? '管理员' : '商家'
})

function handleMenuClick(key: string) {
  router.push(key)
}

function handleLogoutClick() {
  dialog.warning({
    title: '提示',
    content: '确定退出登录吗？',
    positiveText: '确定',
    negativeText: '取消',
    async onPositiveClick() {
      await handleAdminLogout()
      router.replace('/login')
    },
  })
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.logo-wrap {
  height: 64px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  border-bottom: 1px solid #efeff5;
}

.logo-mark {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: linear-gradient(135deg, #2080f0 0%, #4f8df7 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  box-shadow: 0 6px 14px rgba(32, 128, 240, 0.22);
}

.logo-text {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

.header {
  height: 64px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
}

.header-left {
  display: flex;
  align-items: center;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-panel {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 8px 10px 8px 14px;
  border-radius: 999px;
  background: #f8fafc;
  border: 1px solid #edf2f7;
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.role-tag {
  font-weight: 600;
}

.username {
  color: #374151;
  font-size: 14px;
  font-weight: 600;
}

.logout-btn {
  min-width: 88px;
}
</style>