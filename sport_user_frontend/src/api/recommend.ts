import request from './request'
import type { ProductItem } from './product'

export interface RecommendResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface BrowseHistoryItem {
  id: number
  product: ProductItem
  viewed_at: string
}

export interface FavoriteItem {
  id: number
  product: ProductItem
  created_at: string
}

export interface FavoriteStatusData {
  product_id: number
  is_favorite: boolean
}

export interface RecommendProductItem {
  product: ProductItem
  score: number
  source: string
  reason: string
}

export function recordBrowseHistoryApi(productId: number) {
  return request.post<any, RecommendResponse<BrowseHistoryItem>>(
    '/api/recommend/history/record/',
    { product_id: productId },
  )
}

export function getBrowseHistoryListApi() {
  return request.get<any, RecommendResponse<BrowseHistoryItem[]>>(
    '/api/recommend/history/',
  )
}

export function toggleFavoriteApi(productId: number) {
  return request.post<any, RecommendResponse<FavoriteStatusData>>(
    '/api/recommend/favorites/toggle/',
    { product_id: productId },
  )
}

export function getFavoriteStatusApi(productId: number) {
  return request.get<any, RecommendResponse<FavoriteStatusData>>(
    '/api/recommend/favorites/status/',
    {
      params: { product_id: productId },
    },
  )
}

export function getFavoriteListApi() {
  return request.get<any, RecommendResponse<FavoriteItem[]>>(
    '/api/recommend/favorites/',
  )
}

export function getRecommendProductListApi(limit = 6) {
  return request.get<any, RecommendResponse<RecommendProductItem[]>>(
    '/api/recommend/products/',
    {
      params: { limit },
    },
  )
}