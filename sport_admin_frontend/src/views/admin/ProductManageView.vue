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
          <n-button type="primary" @click="fetchList">查询</n-button>
        </n-space>

        <n-button type="primary" @click="openCreate">新增商品</n-button>
      </n-space>
    </n-card>

    <n-card title="商品管理">
      <n-data-table
        :columns="columns"
        :data="tableData"
        :loading="loading"
        :pagination="false"
        :bordered="false"
      />

      <div class="pager-wrap">
        <n-pagination
          v-model:page="page"
          v-model:page-size="pageSize"
          :item-count="total"
          show-size-picker
          :page-sizes="[10, 20, 50]"
          @update:page="fetchList"
          @update:page-size="handlePageSizeChange"
        />
      </div>
    </n-card>

    <n-modal
      v-model:show="showModal"
      preset="card"
      :title="isEdit ? '编辑商品' : '新增商品'"
      style="width: 760px"
    >
      <n-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-placement="left"
        label-width="90"
      >
        <n-grid :cols="2" :x-gap="16">
          <n-form-item-gi label="商品名称" path="name">
            <n-input v-model:value="form.name" />
          </n-form-item-gi>

          <n-form-item-gi label="SKU" path="sku">
            <n-input v-model:value="form.sku" />
          </n-form-item-gi>

          <n-form-item-gi label="分类" path="category">
            <n-select
              v-model:value="form.category"
              :options="categoryOptions"
              label-field="label"
              value-field="value"
            />
          </n-form-item-gi>

          <n-form-item-gi label="品牌">
            <n-input v-model:value="form.brand" />
          </n-form-item-gi>

          <n-form-item-gi label="销售价" path="price">
            <n-input-number v-model:value="form.price" :min="0" style="width: 100%" />
          </n-form-item-gi>

          <n-form-item-gi label="市场价">
            <n-input-number v-model:value="form.market_price" :min="0" style="width: 100%" />
          </n-form-item-gi>

          <n-form-item-gi label="库存" path="stock">
            <n-input-number v-model:value="form.stock" :min="0" style="width: 100%" />
          </n-form-item-gi>

          <n-form-item-gi label="状态" path="status">
            <n-select v-model:value="form.status" :options="statusOptions" />
          </n-form-item-gi>

          <n-form-item-gi :span="2" label="副标题">
            <n-input v-model:value="form.subtitle" />
          </n-form-item-gi>

          <n-form-item-gi :span="2" label="主图地址">
            <n-input v-model:value="form.main_image" />
          </n-form-item-gi>

          <n-form-item-gi :span="2" label="商品描述">
            <n-input v-model:value="form.description" type="textarea" :rows="4" />
          </n-form-item-gi>

          <n-form-item-gi :span="2" label="推荐">
            <n-switch v-model:value="form.is_recommend" />
          </n-form-item-gi>
        </n-grid>
      </n-form>

      <template #footer>
        <n-space justify="end">
          <n-button @click="showModal = false">取消</n-button>
          <n-button type="primary" :loading="submitLoading" @click="handleSubmit">
            保存
          </n-button>
        </n-space>
      </template>
    </n-modal>
  </n-space>
</template>

<script setup lang="ts">
import { h, onMounted, reactive, ref } from 'vue'
import { NButton, NPopconfirm, useMessage, type FormInst, type FormRules } from 'naive-ui'
import {
  createProductApi,
  deleteProductApi,
  getAdminProductListApi,
  getCategoryListApi,
  updateProductApi,
  type CategoryItem,
  type ProductItem,
} from '@/api/product'

const message = useMessage()
const formRef = ref<FormInst | null>(null)

const loading = ref(false)
const submitLoading = ref(false)
const showModal = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)

const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const tableData = ref<ProductItem[]>([])
const categoryOptions = ref<{ label: string; value: number }[]>([])

const query = reactive({
  keyword: '',
  status: null as string | null,
})

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '上架', value: 'on_sale' },
  { label: '下架', value: 'off_sale' },
]

const form = reactive({
  category: null as number | null,
  name: '',
  subtitle: '',
  brand: '',
  sku: '',
  price: 0,
  market_price: 0,
  stock: 0,
  description: '',
  main_image: '',
  status: 'on_sale',
  is_recommend: false,
})

const rules: FormRules = {
  name: { required: true, message: '请输入商品名称', trigger: ['blur', 'input'] },
  sku: { required: true, message: '请输入SKU', trigger: ['blur', 'input'] },
  category: { required: true, type: 'number' as const, message: '请选择分类', trigger: ['change'] },
  price: { required: true, type: 'number' as const, message: '请输入销售价', trigger: ['blur', 'input'] },
  stock: { required: true, type: 'number' as const, message: '请输入库存', trigger: ['blur', 'input'] },
  status: { required: true, message: '请选择状态', trigger: ['change'] },
}

function resetForm() {
  form.category = null
  form.name = ''
  form.subtitle = ''
  form.brand = ''
  form.sku = ''
  form.price = 0
  form.market_price = 0
  form.stock = 0
  form.description = ''
  form.main_image = ''
  form.status = 'on_sale'
  form.is_recommend = false
}

async function fetchCategories() {
  const list = await getCategoryListApi()
  categoryOptions.value = list.map((item: CategoryItem) => ({
    label: item.name,
    value: item.id,
  }))
}

async function fetchList() {
  try {
    loading.value = true
    const res = await getAdminProductListApi({
      page: page.value,
      page_size: pageSize.value,
      keyword: query.keyword,
      status: query.status,
      ordering: '-id',
    })

    tableData.value = res.results.data || []
    total.value = res.count || 0
  } catch (error: any) {
    message.error(error?.response?.data?.message || '获取商品列表失败')
  } finally {
    loading.value = false
  }
}

function handlePageSizeChange() {
  page.value = 1
  fetchList()
}

function openCreate() {
  isEdit.value = false
  editingId.value = null
  resetForm()
  showModal.value = true
}

function openEdit(row: ProductItem) {
  isEdit.value = true
  editingId.value = row.id
  form.category = row.category
  form.name = row.name
  form.subtitle = row.subtitle
  form.brand = row.brand
  form.sku = row.sku
  form.price = Number(row.price)
  form.market_price = Number(row.market_price)
  form.stock = row.stock
  form.description = ''
  form.main_image = row.main_image
  form.status = row.status
  form.is_recommend = row.is_recommend
  showModal.value = true
}

async function handleDelete(row: ProductItem) {
  try {
    await deleteProductApi(row.id)
    message.success('删除成功')
    fetchList()
  } catch (error: any) {
    message.error(error?.response?.data?.message || '删除失败')
  }
}

async function handleSubmit() {
  await formRef.value?.validate()

  try {
    submitLoading.value = true

    const payload = {
      category: form.category!,
      name: form.name,
      subtitle: form.subtitle,
      brand: form.brand,
      sku: form.sku,
      price: form.price,
      market_price: form.market_price,
      stock: form.stock,
      description: form.description,
      main_image: form.main_image,
      status: form.status,
      is_recommend: form.is_recommend,
    }

    if (isEdit.value && editingId.value) {
      await updateProductApi(editingId.value, payload)
      message.success('更新成功')
    } else {
      await createProductApi(payload)
      message.success('创建成功')
    }

    showModal.value = false
    fetchList()
  } catch (error: any) {
    if (error?.response) {
      message.error(error.response.data?.message || '保存失败')
    }
  } finally {
    submitLoading.value = false
  }
}

const columns = [
  { title: 'ID', key: 'id', width: 70 },
  { title: '商品名称', key: 'name' },
  { title: '品牌', key: 'brand', width: 120 },
  { title: 'SKU', key: 'sku', width: 140 },
  { title: '价格', key: 'price', width: 100 },
  { title: '库存', key: 'stock', width: 90 },
  { title: '状态', key: 'status', width: 100 },
  { title: '分类', key: 'category_name', width: 120 },
  {
    title: '操作',
    key: 'actions',
    width: 180,
    render(row: ProductItem) {
      return h('div', { style: 'display:flex; gap:8px;' }, [
        h(
          NButton,
          { size: 'small', onClick: () => openEdit(row) },
          { default: () => '编辑' },
        ),
        h(
          NPopconfirm,
          { onPositiveClick: () => handleDelete(row) },
          {
            trigger: () =>
              h(
                NButton,
                { size: 'small', type: 'error' },
                { default: () => '删除' },
              ),
            default: () => '确定删除该商品吗？',
          },
        ),
      ])
    },
  },
]

onMounted(async () => {
  await fetchCategories()
  await fetchList()
})
</script>

<style scoped>
.pager-wrap {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
