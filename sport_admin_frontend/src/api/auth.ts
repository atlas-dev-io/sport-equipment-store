import request from './request'
import { useAdminUserStore, type AdminUserInfo, type AdminRole } from '@/stores/adminUser'

export interface LoginParams {
  username: string
  password: string
}

export interface LoginResponseData {
  user_id: number
  username: string
  token: string
}

export interface UserMeData {
  id: number
  username: string
  email: string
  is_active: boolean
  date_joined: string
  role: AdminRole | string
  nickname: string
  phone: string
  avatar: string
  gender: string
  birthday: string | null
  address: string
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export function loginApi(data: LoginParams) {
  return request.post<any, ApiResponse<LoginResponseData>>('/api/users/auth/login/', data)
}

export function getCurrentUserApi() {
  return request.get<any, ApiResponse<UserMeData>>('/api/users/auth/me/')
}

export function logoutApi() {
  return request.post<any, ApiResponse<null>>('/api/users/auth/logout/')
}

function normalizeAdminUser(user: UserMeData): AdminUserInfo {
  return {
    id: user.id,
    username: user.username,
    nickname: user.nickname || user.username,
    role: (user.role as AdminRole) || '',
    phone: user.phone || '',
    avatar: user.avatar || '',
    email: user.email || '',
  }
}

export async function handleAdminLogin(data: LoginParams) {
  const adminUserStore = useAdminUserStore()

  const loginRes = await loginApi(data)
  const token = loginRes.data.token

  adminUserStore.setToken(token)

  const meRes = await getCurrentUserApi()
  const me = meRes.data

  if (me.role !== 'merchant' && me.role !== 'admin') {
    adminUserStore.logout()
    throw new Error('当前账号不是商家或管理员，不能进入管理端')
  }

  adminUserStore.setUserInfo(normalizeAdminUser(me))

  return me
}

export async function handleAdminLogout() {
  const adminUserStore = useAdminUserStore()

  try {
    await logoutApi()
  } finally {
    adminUserStore.logout()
  }
}