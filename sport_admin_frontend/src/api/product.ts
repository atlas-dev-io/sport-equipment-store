import request from './request'

export interface CategoryItem {
  id: number
  name: string
  parent: number | null
  sort_order: number
  is_active: boolean
}

export interface ProductItem {
  id: number
  name: string
  subtitle: string
  brand: string
  sku: string
  price: string
  market_price: string
  stock: number
  sales_count: number
  main_image: string
  status: string
  is_recommend: boolean
  category: number
  category_name: string
  created_at: string
  updated_at: string
}

export interface ProductListResponse {
  count: number
  next: string | null
  previous: string | null
  results: {
    code: number
    message: string
    data: ProductItem[]
  }
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface ProductFormData {
  category: number | null
  name: string
  subtitle: string
  brand: string
  sku: string
  price: number | string
  market_price: number | string
  stock: number | string
  description: string
  main_image: string
  status: string
  is_recommend: boolean
}

export function getCategoryListApi() {
  return request.get<any, CategoryItem[]>('/api/products/categories/')
}

export function getAdminProductListApi(params: Record<string, any>) {
  return request.get<any, ProductListResponse>('/api/products/', { params })
}

export function createProductApi(data: ProductFormData) {
  return request.post<any, ApiResponse<ProductItem>>('/api/products/', data)
}

export function updateProductApi(id: number, data: Partial<ProductFormData>) {
  return request.put<any, ApiResponse<ProductItem>>(`/api/products/${id}/`, data)
}

export function deleteProductApi(id: number) {
  return request.delete<any, ApiResponse<null>>(`/api/products/${id}/`)
}