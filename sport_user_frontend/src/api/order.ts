import request from './request'

export interface CreateOrderParams {
  receiver_name: string
  receiver_phone: string
  receiver_address: string
  remark?: string
}

export interface OrderItemSimple {
  id: number
  product: number | null
  product_name: string
  product_image: string
  product_price: string
  quantity: number
  subtotal_amount: string
  created_at: string
}

export interface OrderDetail {
  id: number
  order_no: string
  user: number
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
  items: OrderItemSimple[]
}

export interface OrderResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface PayOrderParams {
  method?: string
}

export interface OrderActionParams {
  remark?: string
}

export function createOrderApi(data: CreateOrderParams) {
  return request.post<any, OrderResponse<OrderDetail>>('/api/orders/create/', data)
}

export function getOrderListApi() {
  return request.get<any, OrderResponse<OrderDetail[]>>('/api/orders/')
}

export function getOrderDetailApi(id: number | string) {
  return request.get<any, OrderResponse<OrderDetail>>(`/api/orders/${id}/`)
}

export function payOrderApi(
  id: number | string,
  data: PayOrderParams = { method: 'mock' },
) {
  return request.post<any, OrderResponse<OrderDetail>>(`/api/orders/${id}/pay/`, data)
}

export function cancelOrderApi(
  id: number | string,
  data: OrderActionParams = {},
) {
  return request.post<any, OrderResponse<OrderDetail>>(`/api/orders/${id}/cancel/`, data)
}

export function completeOrderApi(
  id: number | string,
  data: OrderActionParams = {},
) {
  return request.post<any, OrderResponse<OrderDetail>>(`/api/orders/${id}/complete/`, data)
}