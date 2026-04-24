import request from './request'

export interface ShippingInfo {
  receiver_name: string
  receiver_phone: string
  receiver_address: string
}

export interface ProfileResponse<T = any> {
  code: number
  message: string
  data: T
}

export function getShippingInfoApi() {
  return request.get<any, ProfileResponse<ShippingInfo>>('/api/users/profile/shipping/')
}

export function updateShippingInfoApi(data: ShippingInfo) {
  return request.put<any, ProfileResponse<ShippingInfo>>('/api/users/profile/shipping/', data)
}