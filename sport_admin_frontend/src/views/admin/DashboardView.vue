<template>
  <n-space vertical size="large">
    <n-grid :cols="24" :x-gap="16" :y-gap="16">
      <n-gi :span="6">
        <n-card>
          <n-statistic label="商品数量" :value="overview.product_count" />
        </n-card>
      </n-gi>

      <n-gi :span="6">
        <n-card>
          <n-statistic label="订单数量" :value="overview.order_count" />
        </n-card>
      </n-gi>

      <n-gi :span="6">
        <n-card>
          <n-statistic label="待发货订单" :value="overview.pending_order_count" />
        </n-card>
      </n-gi>

      <n-gi :span="6">
        <n-card>
          <n-statistic label="累计销售额" :value="Number(overview.total_sales_amount || 0)">
            <template #prefix>¥</template>
          </n-statistic>
        </n-card>
      </n-gi>
    </n-grid>

    <n-grid :cols="24" :x-gap="16" :y-gap="16">
      <n-gi :span="12">
        <n-card title="订单状态分布">
          <BaseEChart :option="orderStatusOption" />
        </n-card>
      </n-gi>

      <n-gi :span="12">
        <n-card title="近7天订单趋势">
          <BaseEChart :option="sevenDayTrendOption" />
        </n-card>
      </n-gi>

      <n-gi :span="12">
        <n-card title="分类销量排行">
          <BaseEChart :option="categoryRankingOption" />
        </n-card>
      </n-gi>

      <n-gi :span="12">
        <n-card title="销售额统计">
          <BaseEChart :option="salesStatisticsOption" />
        </n-card>
      </n-gi>
    </n-grid>
  </n-space>
</template>

<script setup lang="ts">
import { computed, reactive } from 'vue'
import { useMessage } from 'naive-ui'
import type { EChartsOption } from 'echarts'
import BaseEChart from '@/components/dashboard/BaseEChart.vue'
import { getAdminDashboardAnalyticsApi } from '@/api/dashboard'

const message = useMessage()

const analytics = reactive({
  overview: {
    product_count: 0,
    order_count: 0,
    pending_order_count: 0,
    today_sales_amount: '0.00',
    seven_day_sales_amount: '0.00',
    total_sales_amount: '0.00',
    role: '' as 'merchant' | 'admin' | '',
  },
  order_status_distribution: [] as Array<{
    status: string
    label: string
    count: number
  }>,
  seven_day_order_trend: [] as Array<{
    date: string
    order_count: number
    sales_amount: string
  }>,
  category_sales_ranking: [] as Array<{
    category_name: string
    sales_quantity: number
    sales_amount: string
  }>,
  sales_statistics: [] as Array<{
    label: string
    value: string
  }>,
})

const overview = computed(() => analytics.overview)

const orderStatusOption = computed<EChartsOption>(() => {
  return {
    tooltip: {
      trigger: 'item',
    },
    legend: {
      bottom: 0,
    },
    series: [
      {
        name: '订单状态',
        type: 'pie',
        radius: ['40%', '68%'],
        center: ['50%', '42%'],
        data: analytics.order_status_distribution.map((item) => ({
          name: item.label,
          value: item.count,
        })),
      },
    ],
  }
})

const sevenDayTrendOption = computed<EChartsOption>(() => {
  return {
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      top: 0,
    },
    grid: {
      left: 48,
      right: 24,
      top: 44,
      bottom: 32,
    },
    xAxis: {
      type: 'category',
      data: analytics.seven_day_order_trend.map((item) => item.date),
    },
    yAxis: [
      {
        type: 'value',
        name: '订单数',
      },
      {
        type: 'value',
        name: '销售额',
      },
    ],
    series: [
      {
        name: '订单数',
        type: 'line',
        smooth: true,
        data: analytics.seven_day_order_trend.map((item) => item.order_count),
      },
      {
        name: '销售额',
        type: 'bar',
        yAxisIndex: 1,
        data: analytics.seven_day_order_trend.map((item) => Number(item.sales_amount || 0)),
      },
    ],
  }
})

const categoryRankingOption = computed<EChartsOption>(() => {
  return {
    tooltip: {
      trigger: 'axis',
    },
    grid: {
      left: 56,
      right: 24,
      top: 24,
      bottom: 32,
    },
    xAxis: {
      type: 'value',
      name: '销售额',
    },
    yAxis: {
      type: 'category',
      data: analytics.category_sales_ranking.map((item) => item.category_name),
    },
    series: [
      {
        name: '销售额',
        type: 'bar',
        data: analytics.category_sales_ranking.map((item) => Number(item.sales_amount || 0)),
      },
    ],
  }
})

const salesStatisticsOption = computed<EChartsOption>(() => {
  return {
    tooltip: {
      trigger: 'axis',
    },
    grid: {
      left: 48,
      right: 24,
      top: 24,
      bottom: 32,
    },
    xAxis: {
      type: 'category',
      data: analytics.sales_statistics.map((item) => item.label),
    },
    yAxis: {
      type: 'value',
      name: '数值',
    },
    series: [
      {
        name: '统计值',
        type: 'bar',
        data: analytics.sales_statistics.map((item) => Number(item.value || 0)),
        barWidth: 36,
      },
    ],
  }
})

async function fetchAnalytics() {
  try {
    const res = await getAdminDashboardAnalyticsApi()

    analytics.overview = res.data.overview
    analytics.order_status_distribution = res.data.order_status_distribution || []
    analytics.seven_day_order_trend = res.data.seven_day_order_trend || []
    analytics.category_sales_ranking = res.data.category_sales_ranking || []
    analytics.sales_statistics = res.data.sales_statistics || []
  } catch (error: any) {
    message.error(error?.response?.data?.message || '获取后台看板数据失败')
  }
}

fetchAnalytics()
</script>