import request from './request'

export interface InventoryProductItem {
  id: number
  name: string
  brand: string
  sku: string
  stock: number
  low_stock_warning: number
  is_low_stock: boolean
  status: string
  category_name: string
  merchant_username: string
  updated_at: string
}

export interface InventoryLogItem {
  id: number
  product: number
  product_name: string
  product_sku: string
  change_type: string
  change_type_label: string
  change_quantity: number
  before_stock: number
  after_stock: number
  remark: string
  operator: number | null
  operator_name: string
  created_at: string
}

export interface InventoryListResponse {
  count: number
  next: string | null
  previous: string | null
  results: {
    code: number
    message: string
    data: InventoryProductItem[]
  }
}

export interface InventoryLogListResponse {
  count: number
  next: string | null
  previous: string | null
  results: {
    code: number
    message: string
    data: InventoryLogItem[]
  }
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface InventoryAdjustPayload {
  change_type: 'increase' | 'decrease'
  quantity: number
  remark?: string
}

export interface InventoryWarningPayload {
  low_stock_warning: number
}

export function getInventoryProductListApi(params: Record<string, any>) {
  return request.get<any, InventoryListResponse>('/api/products/inventory/', { params })
}

export function adjustInventoryApi(id: number, data: InventoryAdjustPayload) {
  return request.post<any, ApiResponse<InventoryProductItem>>(`/api/products/inventory/${id}/adjust/`, data)
}

export function updateLowStockWarningApi(id: number, data: InventoryWarningPayload) {
  return request.patch<any, ApiResponse<InventoryProductItem>>(`/api/products/inventory/${id}/warning/`, data)
}

export function getInventoryLogListApi(params: Record<string, any>) {
  return request.get<any, InventoryLogListResponse>('/api/products/inventory/logs/', { params })
}