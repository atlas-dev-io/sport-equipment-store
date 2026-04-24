<template>
  <div class="page">
    <div class="mobile-shell">
      <div class="top-bar">
        <van-icon name="arrow-left" size="20" @click="goBack" />
        <span class="top-title">收货信息</span>
        <span class="top-placeholder"></span>
      </div>

      <div v-if="loading" class="loading-wrap">
        <van-loading size="24px" vertical>加载中...</van-loading>
      </div>

      <template v-else>
        <div class="card">
          <div class="section-title">默认收货信息</div>

          <van-cell-group inset class="form-group">
            <van-field
              v-model="form.receiver_name"
              label="收货人"
              placeholder="请输入收货人姓名"
              clearable
            />
            <van-field
              v-model="form.receiver_phone"
              label="手机号"
              placeholder="请输入手机号"
              clearable
              type="tel"
            />
            <van-field
              v-model="form.receiver_address"
              label="收货地址"
              placeholder="请输入详细收货地址"
              clearable
              rows="3"
              autosize
              type="textarea"
            />
          </van-cell-group>
        </div>

        <div class="tips-card">
          <div class="tips-title">说明</div>
          <div class="tips-text">
            当前阶段先做一个“默认收货信息”，提交订单时可直接复用。
          </div>
        </div>

        <div class="bottom-safe-space"></div>

        <div class="bottom-action">
          <van-button
            round
            plain
            type="primary"
            class="cancel-btn"
            @click="goBack"
          >
            返回
          </van-button>

          <van-button
            round
            type="primary"
            class="save-btn"
            :loading="saving"
            @click="handleSave"
          >
            保存
          </van-button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast, showSuccessToast } from 'vant'
import { getShippingInfoApi, updateShippingInfoApi } from '@/api/profile'

const router = useRouter()

const loading = ref(false)
const saving = ref(false)

const form = reactive({
  receiver_name: '',
  receiver_phone: '',
  receiver_address: '',
})

function goBack() {
  router.back()
}

function validateForm() {
  if (!form.receiver_name.trim()) {
    showFailToast('请输入收货人姓名')
    return false
  }

  if (!form.receiver_phone.trim()) {
    showFailToast('请输入手机号')
    return false
  }

  if (!/^1\d{10}$/.test(form.receiver_phone.trim())) {
    showFailToast('请输入正确的手机号')
    return false
  }

  if (!form.receiver_address.trim()) {
    showFailToast('请输入收货地址')
    return false
  }

  return true
}

async function fetchShippingInfo() {
  try {
    loading.value = true
    const res = await getShippingInfoApi()

    form.receiver_name = res.data.receiver_name || ''
    form.receiver_phone = res.data.receiver_phone || ''
    form.receiver_address = res.data.receiver_address || ''
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '获取收货信息失败',
    )
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!validateForm()) return

  try {
    saving.value = true

    await updateShippingInfoApi({
      receiver_name: form.receiver_name.trim(),
      receiver_phone: form.receiver_phone.trim(),
      receiver_address: form.receiver_address.trim(),
    })

    showSuccessToast('保存成功')
  } catch (error: any) {
    showFailToast(
      error?.response?.data?.message ||
        error?.response?.data?.detail ||
        '保存收货信息失败',
    )
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchShippingInfo()
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f7fa;
}

.mobile-shell {
  width: 100%;
  max-width: 420px;
  min-height: 100vh;
  margin: 0 auto;
  background: #f5f7fa;
}

.top-bar {
  position: sticky;
  top: 0;
  z-index: 20;
  height: 46px;
  padding: 0 14px;
  background: rgba(255, 255, 255, 0.96);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #edf1f5;
  backdrop-filter: blur(10px);
}

.top-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2d3d;
}

.top-placeholder {
  width: 20px;
}

.loading-wrap {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card,
.tips-card {
  margin: 12px;
  padding: 14px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(31, 45, 61, 0.05);
}

.section-title,
.tips-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2d3d;
  margin-bottom: 12px;
}

.form-group :deep(.van-cell) {
  padding-left: 0;
  padding-right: 0;
}

.tips-text {
  font-size: 13px;
  line-height: 1.8;
  color: #6b7280;
}

.bottom-safe-space {
  height: 80px;
}

.bottom-action {
  position: fixed;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  width: 100%;
  max-width: 420px;
  height: 62px;
  padding: 8px 12px calc(8px + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, 0.98);
  display: flex;
  align-items: center;
  gap: 10px;
  border-top: 1px solid #edf1f5;
  box-sizing: border-box;
}

.cancel-btn,
.save-btn {
  flex: 1;
  height: 40px;
}
</style>