<template>
  <n-space vertical size="large">
    <n-card>
      <n-space justify="space-between" align="center">
        <n-space>
          <n-input
            v-model:value="query.keyword"
            placeholder="搜索商品名称 / SKU / 品牌"
            clearable
            style="width: 260px"
          />
          <n-select
            v-model:value="query.status"
            :options="statusOptions"
            placeholder="商品状态"
            clearable
            style="width: 140px"
          />
          <n-switch v-model:value="query.low_stock_only" />
          <span>只看低库存</span>
          <n-button type="primary" @click="handleQuery">查询</n-button>
        </n-space>

        <n-button @click="fetchInventoryList">刷新库存</n-button>
      </n-space>
    </n-card>

    <n-card title="商品库存列表">
      <n-data-table
        :columns="inventoryColumns"
        :data="inventoryTableData"
        :loading="inventoryLoading"
        :pagination="false"
        :bordered="false"
      />

      <div class="pager-wrap">
        <n-pagination
          v-model:page="inventoryPage"
          v-model:page-size="inventoryPageSize"
          :item-count="inventoryTotal"
          show-size-picker
          :page-sizes="[10, 20, 50]"
          @update:page="fetchInventoryList"
          @update:page-size="handleInventoryPageSizeChange"
        />
      </div>
    </n-card>

    <n-card title="库存变更日志">
      <n-space style="margin-bottom: 16px">
        <n-input
          v-model:value="logQuery.keyword"
          placeholder="搜索日志中的商品名称 / SKU"
          clearable
          style="width: 260px"
        />
        <n-button type="primary" @click="handleLogQuery">查询日志</n-button>
        <n-button v-if="logQuery.product_id" @click="clearLogProductFilter">
          清除商品筛选
        </n-button>
      </n-space>

      <n-data-table
        :columns="logColumns"
        :data="logTableData"
        :loading="logLoading"
        :pagination="false"
        :bordered="false"
      />

      <div class="pager-wrap">
        <n-pagination
          v-model:page="logPage"
          v-model:page-size="logPageSize"
          :item-count="logTotal"
          show-size-picker
          :page-sizes="[10, 20, 50]"
          @update:page="fetchLogList"
          @update:page-size="handleLogPageSizeChange"
        />
      </div>
    </n-card>

    <n-modal
      v-model:show="showAdjustModal"
      preset="card"
      title="手动调整库存"
      style="width: 520px"
    >
      <n-form
        ref="adjustFormRef"
        :model="adjustForm"
        :rules="adjustRules"
        label-placement="left"
        label-width="90"
      >
        <n-form-item label="商品名称">
          <n-input :value="currentProduct?.name || ''" disabled />
        </n-form-item>

        <n-form-item label="当前库存">
          <n-input :value="String(currentProduct?.stock || 0)" disabled />
        </n-form-item>

        <n-form-item label="调整类型" path="change_type">
          <n-select v-model:value="adjustForm.change_type" :options="changeTypeOptions" />
        </n-form-item>

        <n-form-item label="调整数量" path="quantity">
          <n-input-number v-model:value="adjustForm.quantity" :min="1" style="width: 100%" />
        </n-form-item>

        <n-form-item label="备注">
          <n-input v-model:value="adjustForm.remark" type="textarea" :rows="3" />
        </n-form-item>
      </n-form>

      <template #footer>
        <n-space justify="end">
          <n-button @click="showAdjustModal = false">取消</n-button>
          <n-button type="primary" :loading="adjustSubmitting" @click="handleAdjustSubmit">
            确认调整
          </n-button>
        </n-space>
      </template>
    </n-modal>

    <n-modal
      v-model:show="showWarningModal"
      preset="card"
      title="设置低库存预警值"
      style="width: 480px"
    >
      <n-form
        ref="warningFormRef"
        :model="warningForm"
        :rules="warningRules"
        label-placement="left"
        label-width="110"
      >
        <n-form-item label="商品名称">
          <n-input :value="currentProduct?.name || ''" disabled />
        </n-form-item>

        <n-form-item label="当前库存">
          <n-input :value="String(currentProduct?.stock || 0)" disabled />
        </n-form-item>

        <n-form-item label="预警值" path="low_stock_warning">
          <n-input-number
            v-model:value="warningForm.low_stock_warning"
            :min="0"
            style="width: 100%"
          />
        </n-form-item>
      </n-form>

      <template #footer>
        <n-space justify="end">
          <n-button @click="showWarningModal = false">取消</n-button>
          <n-button type="primary" :loading="warningSubmitting" @click="handleWarningSubmit">
            保存
          </n-button>
        </n-space>
      </template>
    </n-modal>
  </n-space>
</template>

<script setup lang="ts">
import { h, onMounted, reactive, ref } from 'vue'
import {
  NButton,
  NPopconfirm,
  NTag,
  useMessage,
  type DataTableColumns,
  type FormInst,
} from 'naive-ui'
import {
  adjustInventoryApi,
  getInventoryLogListApi,
  getInventoryProductListApi,
  updateLowStockWarningApi,
  type InventoryLogItem,
  type InventoryProductItem,
} from '@/api/inventory'

const message = useMessage()

const inventoryLoading = ref(false)
const logLoading = ref(false)

const inventoryPage = ref(1)
const inventoryPageSize = ref(10)
const inventoryTotal = ref(0)

const logPage = ref(1)
const logPageSize = ref(10)
const logTotal = ref(0)

const inventoryTableData = ref<InventoryProductItem[]>([])
const logTableData = ref<InventoryLogItem[]>([])

const query = reactive({
  keyword: '',
  status: null as string | null,
  low_stock_only: false,
})

const logQuery = reactive({
  keyword: '',
  product_id: null as number | null,
})

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '上架', value: 'on_sale' },
  { label: '下架', value: 'off_sale' },
]

const changeTypeOptions = [
  { label: '入库', value: 'increase' },
  { label: '出库', value: 'decrease' },
]

const currentProduct = ref<InventoryProductItem | null>(null)

const showAdjustModal = ref(false)
const adjustSubmitting = ref(false)
const adjustFormRef = ref<FormInst | null>(null)
const adjustForm = reactive({
  change_type: 'increase' as 'increase' | 'decrease',
  quantity: 1 as number | null,
  remark: '',
})

const adjustRules = {
  change_type: {
    required: true,
    message: '请选择调整类型',
    trigger: ['change'],
  },
  quantity: {
    required: true,
    type: 'number',
    message: '请输入调整数量',
    trigger: ['blur', 'input'],
  },
}

const showWarningModal = ref(false)
const warningSubmitting = ref(false)
const warningFormRef = ref<FormInst | null>(null)
const warningForm = reactive({
  low_stock_warning: 10 as number | null,
})

const warningRules = {
  low_stock_warning: {
    required: true,
    type: 'number',
    message: '请输入低库存预警值',
    trigger: ['blur', 'input'],
  },
}

function formatDateTime(value: string) {
  if (!value) return ''
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const mi = String(date.getMinutes()).padStart(2, '0')

  return `${yyyy}-${mm}-${dd} ${hh}:${mi}`
}

function resetAdjustForm() {
  adjustForm.change_type = 'increase'
  adjustForm.quantity = 1
  adjustForm.remark = ''
}

function openAdjustModal(row: InventoryProductItem) {
  currentProduct.value = row
  resetAdjustForm()
  showAdjustModal.value = true
}

function openWarningModal(row: InventoryProductItem) {
  currentProduct.value = row
  warningForm.low_stock_warning = row.low_stock_warning
  showWarningModal.value = true
}

async function handleAdjustSubmit() {
  await adjustFormRef.value?.validate()

  if (!currentProduct.value || !adjustForm.quantity) return

  try {
    adjustSubmitting.value = true

    await adjustInventoryApi(currentProduct.value.id, {
      change_type: adjustForm.change_type,
      quantity: Number(adjustForm.quantity),
      remark: adjustForm.remark.trim(),
    })

    message.success('库存调整成功')
    showAdjustModal.value = false
    await Promise.all([fetchInventoryList(), fetchLogList()])
  } catch (error: any) {
    message.error(error?.response?.data?.message || '库存调整失败')
  } finally {
    adjustSubmitting.value = false
  }
}

async function handleWarningSubmit() {
  await warningFormRef.value?.validate()

  if (!currentProduct.value || warningForm.low_stock_warning === null) return

  try {
    warningSubmitting.value = true

    await updateLowStockWarningApi(currentProduct.value.id, {
      low_stock_warning: Number(warningForm.low_stock_warning),
    })

    message.success('低库存预警值更新成功')
    showWarningModal.value = false
    await fetchInventoryList()
  } catch (error: any) {
    message.error(error?.response?.data?.message || '更新低库存预警值失败')
  } finally {
    warningSubmitting.value = false
  }
}

function handleQuery() {
  inventoryPage.value = 1
  fetchInventoryList()
}

function handleLogQuery() {
  logPage.value = 1
  fetchLogList()
}

function handleInventoryPageSizeChange() {
  inventoryPage.value = 1
  fetchInventoryList()
}

function handleLogPageSizeChange() {
  logPage.value = 1
  fetchLogList()
}

function viewProductLogs(row: InventoryProductItem) {
  logQuery.product_id = row.id
  logPage.value = 1
  fetchLogList()
}

function clearLogProductFilter() {
  logQuery.product_id = null
  logPage.value = 1
  fetchLogList()
}

async function fetchInventoryList() {
  try {
    inventoryLoading.value = true
    const res = await getInventoryProductListApi({
      page: inventoryPage.value,
      page_size: inventoryPageSize.value,
      keyword: query.keyword,
      status: query.status,
      low_stock_only: query.low_stock_only,
    })

    inventoryTableData.value = res.results.data || []
    inventoryTotal.value = res.count || 0
  } catch (error: any) {
    message.error(error?.response?.data?.message || '获取库存商品列表失败')
  } finally {
    inventoryLoading.value = false
  }
}

async function fetchLogList() {
  try {
    logLoading.value = true
    const res = await getInventoryLogListApi({
      page: logPage.value,
      page_size: logPageSize.value,
      keyword: logQuery.keyword,
      product_id: logQuery.product_id,
    })

    logTableData.value = res.results.data || []
    logTotal.value = res.count || 0
  } catch (error: any) {
    message.error(error?.response?.data?.message || '获取库存日志失败')
  } finally {
    logLoading.value = false
  }
}

const inventoryColumns: DataTableColumns<InventoryProductItem> = [
  { title: 'ID', key: 'id', width: 70 },
  { title: '商品名称', key: 'name', minWidth: 180 },
  { title: '品牌', key: 'brand', width: 100, render: (row) => row.brand || '-' },
  { title: 'SKU', key: 'sku', width: 140 },
  { title: '分类', key: 'category_name', width: 120 },
  {
    title: '库存',
    key: 'stock',
    width: 100,
    render: (row) =>
      h(
        NTag,
        { type: row.is_low_stock ? 'error' : 'success', round: true },
        { default: () => `${row.stock}` },
      ),
  },
  { title: '预警值', key: 'low_stock_warning', width: 100 },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render: (row) => {
      const map: Record<string, string> = {
        draft: '草稿',
        on_sale: '上架',
        off_sale: '下架',
      }
      return map[row.status] || row.status
    },
  },
  {
    title: '更新时间',
    key: 'updated_at',
    width: 160,
    render: (row) => formatDateTime(row.updated_at),
  },
  {
    title: '操作',
    key: 'actions',
    width: 280,
    render: (row) =>
      h('div', { style: 'display:flex;gap:8px;flex-wrap:wrap;' }, [
        h(
          NButton,
          {
            size: 'small',
            type: 'primary',
            onClick: () => openAdjustModal(row),
          },
          { default: () => '调整库存' },
        ),
        h(
          NButton,
          {
            size: 'small',
            onClick: () => openWarningModal(row),
          },
          { default: () => '预警设置' },
        ),
        h(
          NButton,
          {
            size: 'small',
            tertiary: true,
            onClick: () => viewProductLogs(row),
          },
          { default: () => '查看日志' },
        ),
      ]),
  },
]

const logColumns: DataTableColumns<InventoryLogItem> = [
  { title: '日志ID', key: 'id', width: 80 },
  { title: '商品名称', key: 'product_name', minWidth: 180 },
  { title: 'SKU', key: 'product_sku', width: 140 },
  {
    title: '变动类型',
    key: 'change_type_label',
    width: 100,
    render: (row) =>
      h(
        NTag,
        {
          type: row.change_type === 'increase' ? 'success' : 'warning',
          round: true,
        },
        { default: () => row.change_type_label },
      ),
  },
  { title: '变动数量', key: 'change_quantity', width: 100 },
  { title: '变动前', key: 'before_stock', width: 90 },
  { title: '变动后', key: 'after_stock', width: 90 },
  { title: '操作人', key: 'operator_name', width: 100, render: (row) => row.operator_name || '-' },
  { title: '备注', key: 'remark', minWidth: 220 },
  {
    title: '时间',
    key: 'created_at',
    width: 160,
    render: (row) => formatDateTime(row.created_at),
  },
]

onMounted(async () => {
  await Promise.all([fetchInventoryList(), fetchLogList()])
})
</script>

<style scoped>
.pager-wrap {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>