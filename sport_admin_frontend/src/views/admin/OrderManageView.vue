<template>
  <n-space vertical size="large">
    <n-card>
      <n-space justify="space-between" align="center">
        <n-space>
          <n-select
            v-model:value="status"
            :options="statusOptions"
            clearable
            placeholder="订单状态"
            style="width: 180px"
          />
          <n-button type="primary" @click="fetchList">查询</n-button>
        </n-space>
      </n-space>
    </n-card>

    <n-card title="订单管理">
      <n-data-table
        :columns="columns"
        :data="tableData"
        :loading="loading"
        :bordered="false"
        :pagination="false"
      />
    </n-card>

    <n-modal
      v-model:show="showShipModal"
      preset="card"
      title="填写物流信息并发货"
      style="width: 560px"
    >
      <n-form
        ref="shipFormRef"
        :model="shipForm"
        :rules="shipRules"
        label-placement="left"
        label-width="90"
      >
        <n-form-item label="订单号">
          <n-input :value="currentOrder?.order_no || ''" disabled />
        </n-form-item>

        <n-form-item label="物流公司" path="shipping_company">
          <n-input v-model:value="shipForm.shipping_company" placeholder="请输入物流公司" />
        </n-form-item>

        <n-form-item label="快递单号" path="tracking_no">
          <n-input v-model:value="shipForm.tracking_no" placeholder="请输入快递单号" />
        </n-form-item>

        <n-form-item label="物流备注">
          <n-input
            v-model:value="shipForm.shipping_remark"
            type="textarea"
            :rows="3"
            placeholder="可选，如发货说明"
          />
        </n-form-item>
      </n-form>

      <template #footer>
        <n-space justify="end">
          <n-button @click="showShipModal = false">取消</n-button>
          <n-button type="primary" :loading="shipSubmitting" @click="handleShipSubmit">
            确认发货
          </n-button>
        </n-space>
      </template>
    </n-modal>
  </n-space>
</template>

<script setup lang="ts">
import { h, onMounted, ref } from 'vue'
import { NButton, NInput, NTag, useMessage, type FormInst } from 'naive-ui'
import {
  getAdminOrderListApi,
  refundOrderApi,
  shipOrderApi,
  type OrderData,
} from '@/api/order'

const message = useMessage()

const loading = ref(false)
const status = ref<string | null>(null)
const tableData = ref<OrderData[]>([])

const showShipModal = ref(false)
const shipSubmitting = ref(false)
const shipFormRef = ref<FormInst | null>(null)
const currentOrder = ref<OrderData | null>(null)

const shipForm = ref({
  shipping_company: '',
  tracking_no: '',
  shipping_remark: '',
})

const shipRules = {
  shipping_company: {
    required: true,
    message: '请输入物流公司',
    trigger: ['blur', 'input'],
  },
  tracking_no: {
    required: true,
    message: '请输入快递单号',
    trigger: ['blur', 'input'],
  },
}

const statusOptions = [
  { label: '待支付', value: 'pending_payment' },
  { label: '已支付', value: 'paid' },
  { label: '已发货', value: 'shipped' },
  { label: '已完成', value: 'completed' },
  { label: '已取消', value: 'canceled' },
  { label: '已退款', value: 'refunded' },
]

function statusLabel(value: string) {
  const map: Record<string, string> = {
    pending_payment: '待支付',
    paid: '已支付',
    shipped: '已发货',
    completed: '已完成',
    canceled: '已取消',
    refunded: '已退款',
  }
  return map[value] || value
}

function statusType(value: string) {
  const map: Record<string, any> = {
    pending_payment: 'warning',
    paid: 'info',
    shipped: 'primary',
    completed: 'success',
    canceled: 'default',
    refunded: 'error',
  }
  return map[value] || 'default'
}

function openShipModal(row: OrderData) {
  currentOrder.value = row
  shipForm.value = {
    shipping_company: row.shipping_company || '',
    tracking_no: row.tracking_no || '',
    shipping_remark: row.shipping_remark || '',
  }
  showShipModal.value = true
}

async function handleShipSubmit() {
  await shipFormRef.value?.validate()

  if (!currentOrder.value) return

  try {
    shipSubmitting.value = true
    await shipOrderApi(currentOrder.value.id, {
      shipping_company: shipForm.value.shipping_company.trim(),
      tracking_no: shipForm.value.tracking_no.trim(),
      shipping_remark: shipForm.value.shipping_remark.trim(),
    })
    message.success('发货成功')
    showShipModal.value = false
    fetchList()
  } catch (error: any) {
    message.error(error?.response?.data?.message || '发货失败')
  } finally {
    shipSubmitting.value = false
  }
}

async function handleRefund(row: OrderData) {
  try {
    await refundOrderApi(row.id, '后台操作退款')
    message.success('退款成功')
    fetchList()
  } catch (error: any) {
    message.error(error?.response?.data?.message || '退款失败')
  }
}

async function fetchList() {
  try {
    loading.value = true
    const res = await getAdminOrderListApi({
      status: status.value || undefined,
    })
    tableData.value = res.data || []
  } catch (error: any) {
    message.error(error?.response?.data?.message || '获取订单失败')
  } finally {
    loading.value = false
  }
}

const columns = [
  { title: '订单号', key: 'order_no', width: 220 },
  { title: '用户', key: 'username', width: 120 },
  {
    title: '状态',
    key: 'status',
    width: 110,
    render(row: OrderData) {
      return h(
        NTag,
        { type: statusType(row.status), size: 'small' },
        { default: () => statusLabel(row.status) },
      )
    },
  },
  { title: '收货人', key: 'receiver_name', width: 100 },
  { title: '手机号', key: 'receiver_phone', width: 130 },
  { title: '金额', key: 'total_amount', width: 100 },
  {
    title: '物流信息',
    key: 'shipping',
    width: 220,
    render(row: OrderData) {
      if (!row.shipping_company && !row.tracking_no) return '-'
      return `${row.shipping_company || '-'} / ${row.tracking_no || '-'}`
    },
  },
  {
    title: '商品',
    key: 'items',
    render(row: OrderData) {
      return row.items.map((item) => `${item.product_name} x${item.quantity}`).join('；')
    },
  },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    render(row: OrderData) {
      const actions = []

      if (row.status === 'paid') {
        actions.push(
          h(
            NButton,
            {
              type: 'primary',
              size: 'small',
              style: 'margin-right:8px;',
              onClick: () => openShipModal(row),
            },
            { default: () => '发货' },
          ),
        )
        actions.push(
          h(
            NButton,
            {
              type: 'error',
              size: 'small',
              ghost: true,
              onClick: () => handleRefund(row),
            },
            { default: () => '退款' },
          ),
        )
      }

      return h('div', actions)
    },
  },
]

onMounted(() => {
  fetchList()
})
</script>