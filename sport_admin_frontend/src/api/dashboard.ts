import request from './request'

export interface DashboardOverview {
  product_count: number
  order_count: number
  pending_order_count: number
  today_sales_amount: string
  seven_day_sales_amount: string
  total_sales_amount: string
  role: 'merchant' | 'admin' | ''
}

export interface OrderStatusDistributionItem {
  status: string
  label: string
  count: number
}

export interface SevenDayTrendItem {
  date: string
  order_count: number
  sales_amount: string
}

export interface CategorySalesRankingItem {
  category_name: string
  sales_quantity: number
  sales_amount: string
}

export interface SalesStatisticsItem {
  label: string
  value: string
}

export interface AdminDashboardAnalytics {
  overview: DashboardOverview
  order_status_distribution: OrderStatusDistributionItem[]
  seven_day_order_trend: SevenDayTrendItem[]
  category_sales_ranking: CategorySalesRankingItem[]
  sales_statistics: SalesStatisticsItem[]
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export function getAdminDashboardStatsApi() {
  return request.get<any, ApiResponse<DashboardOverview>>('/api/dashboard/admin/stats/')
}

export function getAdminDashboardAnalyticsApi() {
  return request.get<any, ApiResponse<AdminDashboardAnalytics>>('/api/dashboard/admin/analytics/')
}