import request from './request'

export interface ProfileInfo {
  username: string
  nickname: string
  phone: string
  email: string
  avatar: string
  role: string
}

export interface ProfileInfoResponse<T = any> {
  code: number
  message: string
  data: T
}

export function getProfileInfoApi() {
  return request.get<any, ProfileInfoResponse<ProfileInfo>>('/api/users/profile/info/')
}

export function updateProfileInfoApi(data: Partial<ProfileInfo>) {
  return request.put<any, ProfileInfoResponse<ProfileInfo>>('/api/users/profile/info/', data)
}