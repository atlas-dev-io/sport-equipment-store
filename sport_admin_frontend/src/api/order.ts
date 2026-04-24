import request from './request'

export interface OrderItem {
  id: number
  product: number | null
  product_name: string
  product_image: string
  product_price: string
  quantity: number
  subtotal_amount: string
  created_at: string
  merchant_id: number | null
  merchant_username: string
}

export interface OrderData {
  id: number
  order_no: string
  user: number
  username: string
  status: string
  total_amount: string
  pay_amount: string
  receiver_name: string
  receiver_phone: string
  receiver_address: string
  remark: string
  shipping_company: string
  tracking_no: string
  shipping_remark: string
  paid_at: string | null
  shipped_at: string | null
  completed_at: string | null
  created_at: string
  updated_at: string
  items: OrderItem[]
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export function getAdminOrderListApi(params?: Record<string, any>) {
  return request.get<any, ApiResponse<OrderData[]>>('/api/orders/', { params })
}

export function shipOrderApi(
  id: number,
  data: {
    shipping_company: string
    tracking_no: string
    shipping_remark?: string
  },
) {
  return request.post<any, ApiResponse<OrderData>>(`/api/orders/${id}/ship/`, data)
}

export function refundOrderApi(id: number, remark = '') {
  return request.post<any, ApiResponse<OrderData>>(`/api/orders/${id}/refund/`, { remark })
}