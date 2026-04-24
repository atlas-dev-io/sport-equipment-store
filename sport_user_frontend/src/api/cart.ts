import request from './request'

export interface CartProduct {
  id: number
  name: string
  subtitle: string
  brand: string
  sku: string
  price: string
  market_price: string
  stock: number
  main_image: string
  status: string
  category: number
  category_name: string
}

export interface CartItem {
  id: number
  product: CartProduct
  quantity: number
  checked: boolean
  subtotal: string
  created_at: string
  updated_at: string
}

export interface CartDetailData {
  id: number
  user: number
  items: CartItem[]
  total_count: number
  checked_count: number
  total_amount: string
  checked_amount: string
  created_at: string
  updated_at: string
}

export interface CartResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface AddCartItemParams {
  product_id: number
  quantity: number
}

export interface UpdateCartItemParams {
  quantity?: number
  checked?: boolean
}

export function getCartDetailApi() {
  return request.get<any, CartResponse<CartDetailData>>('/api/cart/')
}

export function addCartItemApi(data: AddCartItemParams) {
  return request.post<any, CartResponse<CartItem>>('/api/cart/items/', data)
}

export function updateCartItemApi(id: number, data: UpdateCartItemParams) {
  return request.patch<any, CartResponse<CartItem>>(`/api/cart/items/${id}/`, data)
}

export function deleteCartItemApi(id: number) {
  return request.delete<any, CartResponse<null>>(`/api/cart/items/${id}/`)
}

export function clearCartApi() {
  return request.post<any, CartResponse<null>>('/api/cart/clear/')
}