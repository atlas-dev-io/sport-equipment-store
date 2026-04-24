<template>
  <n-space vertical size="large">
    <n-card>
      <n-space justify="space-between" align="center">
        <n-space>
          <n-input
            v-model:value="query.keyword"
            placeholder="搜索用户名"
            clearable
            style="width: 220px"
          />
          <n-select
            v-model:value="query.role"
            :options="roleOptions"
            placeholder="角色"
            clearable
            style="width: 160px"
          />
          <n-select
            v-model:value="query.is_active"
            :options="activeOptions"
            placeholder="状态"
            clearable
            style="width: 160px"
          />
          <n-button type="primary" @click="fetchList">查询</n-button>
        </n-space>
      </n-space>
    </n-card>

    <n-card title="用户管理">
      <n-data-table
        :columns="columns"
        :data="tableData"
        :loading="loading"
        :bordered="false"
        :pagination="false"
      />
    </n-card>

    <n-card title="商家申请审核">
      <n-space style="margin-bottom: 16px">
        <n-input
          v-model:value="applicationQuery.keyword"
          placeholder="搜索用户名 / 店铺名称 / 联系人 / 手机号"
          clearable
          style="width: 320px"
        />
        <n-select
          v-model:value="applicationQuery.status"
          :options="applicationStatusOptions"
          placeholder="审核状态"
          clearable
          style="width: 160px"
        />
        <n-button type="primary" @click="fetchApplicationList">查询</n-button>
      </n-space>

      <n-data-table
        :columns="applicationColumns"
        :data="applicationTableData"
        :loading="applicationLoading"
        :bordered="false"
        :pagination="false"
      />
    </n-card>

    <n-modal
      v-model:show="showModal"
      preset="card"
      title="编辑用户"
      style="width: 640px"
    >
      <n-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-placement="left"
        label-width="90"
      >
        <n-form-item label="用户名">
          <n-input v-model:value="form.username" readonly />
        </n-form-item>

        <n-form-item label="昵称" path="nickname">
          <n-input v-model:value="form.nickname" />
        </n-form-item>

        <n-form-item label="手机号" path="phone">
          <n-input v-model:value="form.phone" />
        </n-form-item>

        <n-form-item label="邮箱" path="email">
          <n-input v-model:value="form.email" />
        </n-form-item>

        <n-form-item label="角色" path="role">
          <n-select v-model:value="form.role" :options="roleOptions" />
        </n-form-item>

        <n-form-item label="启用状态" path="is_active">
          <n-switch v-model:value="form.is_active" />
        </n-form-item>
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

    <n-modal
      v-model:show="showReviewModal"
      preset="card"
      title="审核商家申请"
      style="width: 680px"
    >
      <n-form
        ref="reviewFormRef"
        :model="reviewForm"
        label-placement="left"
        label-width="100"
      >
        <n-form-item label="申请用户">
          <n-input :value="currentApplication?.username || ''" readonly />
        </n-form-item>

        <n-form-item label="店铺名称">
          <n-input :value="currentApplication?.shop_name || ''" readonly />
        </n-form-item>

        <n-form-item label="联系人">
          <n-input :value="currentApplication?.contact_name || ''" readonly />
        </n-form-item>

        <n-form-item label="联系电话">
          <n-input :value="currentApplication?.contact_phone || ''" readonly />
        </n-form-item>

        <n-form-item label="申请说明">
          <n-input
            :value="currentApplication?.application_reason || ''"
            type="textarea"
            :rows="4"
            readonly
          />
        </n-form-item>

        <n-form-item label="审核备注">
          <n-input
            v-model:value="reviewForm.review_remark"
            type="textarea"
            :rows="3"
            placeholder="可填写通过说明或拒绝原因"
          />
        </n-form-item>
      </n-form>

      <template #footer>
        <n-space justify="end">
          <n-button @click="showReviewModal = false">取消</n-button>
          <n-button
            type="error"
            ghost
            :loading="reviewSubmitting"
            @click="handleReview('rejected')"
          >
            拒绝
          </n-button>
          <n-button
            type="primary"
            :loading="reviewSubmitting"
            @click="handleReview('approved')"
          >
            通过
          </n-button>
        </n-space>
      </template>
    </n-modal>
  </n-space>
</template>

<script setup lang="ts">
import { h, onMounted, reactive, ref } from 'vue'
import { NButton, NInput, NTag, useMessage, type FormInst } from 'naive-ui'
import {
  getAdminUserListApi,
  getMerchantApplicationListApi,
  reviewMerchantApplicationApi,
  updateAdminUserApi,
  type AdminUserItem,
  type MerchantApplicationItem,
} from '@/api/adminUser'

const message = useMessage()
const formRef = ref<FormInst | null>(null)
const reviewFormRef = ref<FormInst | null>(null)

const loading = ref(false)
const submitLoading = ref(false)
const applicationLoading = ref(false)
const reviewSubmitting = ref(false)

const showModal = ref(false)
const showReviewModal = ref(false)

const editingId = ref<number | null>(null)
const tableData = ref<AdminUserItem[]>([])
const applicationTableData = ref<MerchantApplicationItem[]>([])
const currentApplication = ref<MerchantApplicationItem | null>(null)

const query = reactive({
  keyword: '',
  role: null as string | null,
  is_active: null as string | null,
})

const applicationQuery = reactive({
  keyword: '',
  status: 'pending' as string | null,
})

const form = reactive({
  username: '',
  nickname: '',
  phone: '',
  email: '',
  role: 'customer' as 'customer' | 'merchant' | 'admin',
  is_active: true,
})

const reviewForm = reactive({
  review_remark: '',
})

const roleOptions = [
  { label: '普通用户', value: 'customer' },
  { label: '商家', value: 'merchant' },
  { label: '管理员', value: 'admin' },
]

const activeOptions = [
  { label: '启用', value: 'true' },
  { label: '禁用', value: 'false' },
]

const applicationStatusOptions = [
  { label: '待审核', value: 'pending' },
  { label: '已通过', value: 'approved' },
  { label: '已拒绝', value: 'rejected' },
]

const rules = {
  role: { required: true, message: '请选择角色', trigger: ['change'] },
}

function roleText(role: string) {
  const map: Record<string, string> = {
    customer: '普通用户',
    merchant: '商家',
    admin: '管理员',
  }
  return map[role] || role
}

function applicationStatusText(status: string) {
  const map: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
  }
  return map[status] || status
}

function formatDateTime(value?: string | null) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(
    date.getDate(),
  ).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(
    date.getMinutes(),
  ).padStart(2, '0')}`
}

async function fetchList() {
  try {
    loading.value = true
    const res = await getAdminUserListApi({
      keyword: query.keyword || undefined,
      role: query.role || undefined,
      is_active: query.is_active || undefined,
    })
    tableData.value = res.data || []
  } catch (error: any) {
    message.error(error?.response?.data?.message || '获取用户列表失败')
  } finally {
    loading.value = false
  }
}

async function fetchApplicationList() {
  try {
    applicationLoading.value = true
    const res = await getMerchantApplicationListApi({
      keyword: applicationQuery.keyword || undefined,
      status: applicationQuery.status || undefined,
    })
    applicationTableData.value = res.data || []
  } catch (error: any) {
    message.error(error?.response?.data?.message || '获取商家申请列表失败')
  } finally {
    applicationLoading.value = false
  }
}

function openEdit(row: AdminUserItem) {
  editingId.value = row.id
  form.username = row.username
  form.nickname = row.nickname || ''
  form.phone = row.phone || ''
  form.email = row.email || ''
  form.role = row.role
  form.is_active = row.is_active
  showModal.value = true
}

function openReview(row: MerchantApplicationItem) {
  currentApplication.value = row
  reviewForm.review_remark = row.review_remark || ''
  showReviewModal.value = true
}

async function handleSubmit() {
  await formRef.value?.validate()

  if (!editingId.value) return

  try {
    submitLoading.value = true
    await updateAdminUserApi(editingId.value, {
      nickname: form.nickname,
      phone: form.phone,
      email: form.email,
      role: form.role,
      is_active: form.is_active,
    })
    message.success('更新成功')
    showModal.value = false
    fetchList()
  } catch (error: any) {
    message.error(error?.response?.data?.message || '更新失败')
  } finally {
    submitLoading.value = false
  }
}

async function handleReview(action: 'approved' | 'rejected') {
  if (!currentApplication.value) return

  try {
    reviewSubmitting.value = true
    await reviewMerchantApplicationApi(currentApplication.value.id, {
      action,
      review_remark: reviewForm.review_remark,
    })
    message.success(action === 'approved' ? '审核通过成功' : '审核拒绝成功')
    showReviewModal.value = false
    fetchApplicationList()
    fetchList()
  } catch (error: any) {
    message.error(error?.response?.data?.message || '审核失败')
  } finally {
    reviewSubmitting.value = false
  }
}

const columns = [
  { title: 'ID', key: 'id', width: 70 },
  { title: '用户名', key: 'username', width: 120 },
  { title: '昵称', key: 'nickname', width: 120 },
  { title: '手机号', key: 'phone', width: 130 },
  { title: '邮箱', key: 'email', width: 180 },
  {
    title: '角色',
    key: 'role',
    width: 100,
    render(row: AdminUserItem) {
      return h(
        NTag,
        {
          type: row.role === 'admin' ? 'error' : row.role === 'merchant' ? 'warning' : 'default',
          size: 'small',
        },
        { default: () => roleText(row.role) },
      )
    },
  },
  {
    title: '状态',
    key: 'is_active',
    width: 90,
    render(row: AdminUserItem) {
      return h(
        NTag,
        { type: row.is_active ? 'success' : 'default', size: 'small' },
        { default: () => (row.is_active ? '启用' : '禁用') },
      )
    },
  },
  { title: '注册时间', key: 'date_joined', width: 180, render: (row: AdminUserItem) => formatDateTime(row.date_joined) },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render(row: AdminUserItem) {
      return h(
        NButton,
        {
          size: 'small',
          type: 'primary',
          onClick: () => openEdit(row),
        },
        { default: () => '编辑' },
      )
    },
  },
]

const applicationColumns = [
  { title: '申请ID', key: 'id', width: 80 },
  { title: '用户名', key: 'username', width: 120 },
  { title: '店铺名称', key: 'shop_name', width: 160 },
  { title: '联系人', key: 'contact_name', width: 100 },
  { title: '联系电话', key: 'contact_phone', width: 130 },
  { title: '申请说明', key: 'application_reason' },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render(row: MerchantApplicationItem) {
      const type =
        row.status === 'approved' ? 'success' : row.status === 'rejected' ? 'error' : 'warning'
      return h(
        NTag,
        { type, size: 'small' },
        { default: () => applicationStatusText(row.status) },
      )
    },
  },
  { title: '审核备注', key: 'review_remark', width: 180, render: (row: MerchantApplicationItem) => row.review_remark || '-' },
  { title: '申请时间', key: 'created_at', width: 180, render: (row: MerchantApplicationItem) => formatDateTime(row.created_at) },
  {
    title: '操作',
    key: 'actions',
    width: 120,
    render(row: MerchantApplicationItem) {
      if (row.status !== 'pending') {
        return '-'
      }
      return h(
        NButton,
        {
          size: 'small',
          type: 'primary',
          onClick: () => openReview(row),
        },
        { default: () => '审核' },
      )
    },
  },
]

onMounted(() => {
  fetchList()
  fetchApplicationList()
})
</script>