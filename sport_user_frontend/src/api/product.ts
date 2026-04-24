import request from './request'

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

export interface ProductListInnerData {
  code: number
  message: string
  data: ProductItem[]
}

export interface ProductListResponse {
  count: number
  next: string | null
  previous: string | null
  results: ProductListInnerData
}

export interface ProductListParams {
  page?: number
  page_size?: number
  keyword?: string
  category?: number | string
  brand?: string
  min_price?: number | string
  max_price?: number | string
  is_recommend?: boolean | string
  ordering?: string
}

export interface ProductDetailCategory {
  id: number
  name: string
  parent: number | null
  sort_order: number
  is_active: boolean
}

export interface ProductImageItem {
  id: number
  image_url: string
  alt_text: string
  sort_order: number
  is_main: boolean
  created_at: string
}

export interface ProductDetail {
  id: number
  name: string
  subtitle: string
  brand: string
  sku: string
  price: string
  market_price: string
  stock: number
  sales_count: number
  description: string
  main_image: string
  status: string
  is_recommend: boolean
  merchant: number | null
  merchant_username: string
  category: ProductDetailCategory
  images: ProductImageItem[]
  created_at: string
  updated_at: string
}

export interface ProductDetailResponse {
  code: number
  message: string
  data: ProductDetail
}

export function getProductListApi(params: ProductListParams) {
  const finalParams = {
    ...params,
    is_recommend:
      typeof params.is_recommend === 'boolean'
        ? params.is_recommend
          ? 'true'
          : ''
        : params.is_recommend,
  }

  return request.get<any, ProductListResponse>('/api/products/', {
    params: finalParams,
  })
}

export function getProductDetailApi(id: number | string) {
  return request.get<any, ProductDetailResponse>(`/api/products/${id}/`)
}