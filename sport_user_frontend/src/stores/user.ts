import { defineStore } from 'pinia'

export interface CurrentUser {
  id: number | string
  username: string
  nickname?: string
  phone?: string
  avatar?: string
  role?: string
  merchant_application_status?: string
  merchant_application_shop_name?: string
  merchant_application_review_remark?: string
}

interface UserState {
  token: string
  currentUser: CurrentUser | null
}

const TOKEN_KEY = 'sport_user_token'
const USER_KEY = 'sport_current_user'

function getLocalToken(): string {
  return localStorage.getItem(TOKEN_KEY) || ''
}

function getLocalUser(): CurrentUser | null {
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null

  try {
    return JSON.parse(raw) as CurrentUser
  } catch (error) {
    localStorage.removeItem(USER_KEY)
    return null
  }
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    token: getLocalToken(),
    currentUser: getLocalUser(),
  }),

  getters: {
    isLogin: (state) => !!state.token,
  },

  actions: {
    setToken(token: string) {
      this.token = token
      localStorage.setItem(TOKEN_KEY, token)
    },

    clearToken() {
      this.token = ''
      localStorage.removeItem(TOKEN_KEY)
    },

    setCurrentUser(user: CurrentUser | null) {
      this.currentUser = user

      if (user) {
        localStorage.setItem(USER_KEY, JSON.stringify(user))
      } else {
        localStorage.removeItem(USER_KEY)
      }
    },

    login(payload: { token: string; user: CurrentUser }) {
      this.setToken(payload.token)
      this.setCurrentUser(payload.user)
    },

    logout() {
      this.clearToken()
      this.setCurrentUser(null)
    },
  },
})