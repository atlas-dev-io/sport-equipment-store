import request from './request'

export interface AdminUserItem {
  id: number
  username: string
  email: string
  is_active: boolean
  date_joined: string
  nickname: string
  phone: string
  role: 'customer' | 'merchant' | 'admin'
  avatar: string
}

export interface MerchantApplicationItem {
  id: number
  user: number
  username: string
  shop_name: string
  contact_name: string
  contact_phone: string
  application_reason: string
  status: 'pending' | 'approved' | 'rejected'
  review_remark: string
  reviewed_by: number | null
  reviewed_by_username: string
  reviewed_at: string | null
  created_at: string
  updated_at: string
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export function getAdminUserListApi(params?: Record<string, any>) {
  return request.get<any, ApiResponse<AdminUserItem[]>>('/api/users/admin/users/', { params })
}

export function updateAdminUserApi(id: number, data: Record<string, any>) {
  return request.put<any, ApiResponse<AdminUserItem>>(`/api/users/admin/users/${id}/`, data)
}

export function getMerchantApplicationListApi(params?: Record<string, any>) {
  return request.get<any, ApiResponse<MerchantApplicationItem[]>>('/api/users/admin/merchant-applications/', { params })
}

export function reviewMerchantApplicationApi(
  id: number,
  data: {
    action: 'approved' | 'rejected'
    review_remark?: string
  },
) {
  return request.post<any, ApiResponse<MerchantApplicationItem>>(
    `/api/users/admin/merchant-applications/${id}/review/`,
    data,
  )
}