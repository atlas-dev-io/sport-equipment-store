import { defineStore } from 'pinia'

export type AdminRole = 'merchant' | 'admin' | ''

export interface AdminUserInfo {
  id: number | string
  username: string
  nickname?: string
  role: AdminRole
  phone?: string
  avatar?: string
  email?: string
}

interface AdminUserState {
  token: string
  userInfo: AdminUserInfo | null
}

const TOKEN_KEY = 'sport_admin_token'
const USER_KEY = 'sport_admin_user'

function getLocalToken(): string {
  return localStorage.getItem(TOKEN_KEY) || ''
}

function getLocalUser(): AdminUserInfo | null {
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null

  try {
    return JSON.parse(raw) as AdminUserInfo
  } catch {
    localStorage.removeItem(USER_KEY)
    return null
  }
}

export const useAdminUserStore = defineStore('adminUser', {
  state: (): AdminUserState => ({
    token: getLocalToken(),
    userInfo: getLocalUser(),
  }),

  getters: {
    isLogin: (state) => !!state.token,
    role: (state) => state.userInfo?.role || '',
    username: (state) => state.userInfo?.nickname || state.userInfo?.username || '未登录',
  },

  actions: {
    setToken(token: string) {
      this.token = token
      localStorage.setItem(TOKEN_KEY, token)
    },

    setUserInfo(userInfo: AdminUserInfo | null) {
      this.userInfo = userInfo
      if (userInfo) {
        localStorage.setItem(USER_KEY, JSON.stringify(userInfo))
      } else {
        localStorage.removeItem(USER_KEY)
      }
    },

    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
    },
  },
})