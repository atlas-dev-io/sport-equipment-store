import request, { type ApiResponse } from './request'
import { useUserStore, type CurrentUser } from '@/stores/user'

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  phone?: string
  password: string
  confirm_password: string
  nickname?: string
  email?: string
  role?: string
}

export interface MerchantApplicationParams {
  shop_name: string
  contact_name: string
  contact_phone: string
  application_reason?: string
}

interface LoginData {
  user_id: number
  username: string
  token: string
}

interface RegisterData {
  user_id: number
  username: string
  token: string
}

export function loginApi(data: LoginParams) {
  return request.post<any, ApiResponse<LoginData>>('/api/users/auth/login/', data)
}

export function registerApi(data: RegisterParams) {
  return request.post<any, ApiResponse<RegisterData>>('/api/users/auth/register/', data)
}

export function getCurrentUserApi() {
  return request.get<any, ApiResponse<CurrentUser>>('/api/users/auth/me/')
}

export function logoutApi() {
  return request.post('/api/users/auth/logout/')
}

export function becomeMerchantApi(data: MerchantApplicationParams) {
  return request.post<any, ApiResponse<any>>('/api/users/profile/become-merchant/', data)
}

export async function handleLogin(data: LoginParams) {
  const userStore = useUserStore()

  const loginRes = await loginApi(data)
  const token = loginRes.data.token

  userStore.setToken(token)

  const meRes = await getCurrentUserApi()
  userStore.setCurrentUser(meRes.data)

  return meRes.data
}

export async function handleRegister(data: RegisterParams) {
  return await registerApi(data)
}

export async function handleLogout() {
  const userStore = useUserStore()

  try {
    await logoutApi()
  } finally {
    userStore.logout()
  }
}