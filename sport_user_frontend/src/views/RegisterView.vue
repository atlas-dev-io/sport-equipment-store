<template>
  <div class="register-page">
    <div class="header-area">
      <div class="header-content">
        <div class="mini-badge">新用户注册</div>
        <h1 class="title">欢迎加入运动装备商城</h1>
        <p class="subtitle">注册后即可浏览商品、加入购物车并管理个人订单</p>
      </div>
    </div>

    <div class="register-card">
      <div class="form-title">创建账户</div>
      <div class="form-desc">请填写基础信息，完成账号注册</div>

      <van-field
        v-model="form.username"
        class="custom-field"
        label="用户名"
        placeholder="请输入用户名"
        clearable
      >
        <template #left-icon>
          <van-icon name="user-o" />
        </template>
      </van-field>

      <van-field
        v-model="form.phone"
        class="custom-field"
        label="手机号"
        placeholder="请输入手机号"
        clearable
      >
        <template #left-icon>
          <van-icon name="phone-o" />
        </template>
      </van-field>

      <van-field
        v-model="form.password"
        class="custom-field"
        type="password"
        label="密码"
        placeholder="请输入登录密码"
        clearable
      >
        <template #left-icon>
          <van-icon name="lock" />
        </template>
      </van-field>

      <van-field
        v-model="form.confirmPassword"
        class="custom-field"
        type="password"
        label="确认密码"
        placeholder="请再次输入密码"
        clearable
        @keyup.enter="onRegister"
      >
        <template #left-icon>
          <van-icon name="shield-o" />
        </template>
      </van-field>

      <van-field
        v-model="form.inviteCode"
        class="custom-field"
        label="邀请码"
        placeholder="选填"
        clearable
      >
        <template #left-icon>
          <van-icon name="gift-o" />
        </template>
      </van-field>

      <div class="agreement-row">
        <span class="agreement-text">
          注册即表示同意《用户协议》与《隐私政策》
        </span>
      </div>

      <div class="btn-group">
        <van-button
          type="primary"
          block
          round
          class="submit-btn"
          :loading="loading"
          @click="onRegister"
        >
          立即注册
        </van-button>

        <van-button
          plain
          block
          round
          class="back-btn"
          @click="goLogin"
        >
          返回登录
        </van-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast, showSuccessToast } from 'vant'
import { handleRegister } from '@/api/auth'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  username: '',
  phone: '',
  password: '',
  confirmPassword: '',
  inviteCode: '',
})

function goLogin() {
  router.push('/login')
}

async function onRegister() {
  if (!form.username.trim()) {
    showFailToast('请输入用户名')
    return
  }

  if (!form.phone.trim()) {
    showFailToast('请输入手机号')
    return
  }

  if (!/^1\d{10}$/.test(form.phone.trim())) {
    showFailToast('请输入正确的手机号')
    return
  }

  if (!form.password.trim()) {
    showFailToast('请输入密码')
    return
  }

  if (form.password.length < 6) {
    showFailToast('密码长度不能少于6位')
    return
  }

  if (!form.confirmPassword.trim()) {
    showFailToast('请输入确认密码')
    return
  }

  if (form.password !== form.confirmPassword) {
    showFailToast('两次输入的密码不一致')
    return
  }

  try {
    loading.value = true

    await handleRegister({
      username: form.username.trim(),
      phone: form.phone.trim(),
      password: form.password,
      confirm_password: form.confirmPassword,
      role: 'customer',
    })

    showSuccessToast('注册成功，请登录')

    router.replace('/login')
  } catch (error: any) {
    const message =
      error?.response?.data?.message ||
      error?.response?.data?.detail ||
      '注册失败，请检查输入信息'
    showFailToast(message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #eef7ff 0%, #f8fbff 36%, #f5f7fa 100%);
}

.header-area {
  padding: 28px 18px 88px;
  background: linear-gradient(135deg, #1989fa 0%, #69b8ff 100%);
  border-bottom-left-radius: 28px;
  border-bottom-right-radius: 28px;
  box-shadow: 0 8px 24px rgba(25, 137, 250, 0.18);
}

.header-content {
  color: #fff;
}

.mini-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.18);
  font-size: 12px;
  margin-bottom: 12px;
}

.title {
  margin: 0;
  font-size: 24px;
  line-height: 1.4;
  font-weight: 700;
}

.subtitle {
  margin: 10px 0 0;
  font-size: 13px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.92);
}

.register-card {
  width: calc(100% - 32px);
  margin: -58px auto 0;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 12px 30px rgba(38, 80, 120, 0.08);
  padding: 22px 18px 24px;
  box-sizing: border-box;
}

.form-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2d3d;
}

.form-desc {
  margin-top: 8px;
  margin-bottom: 18px;
  font-size: 13px;
  color: #7f8b96;
  line-height: 1.6;
}

.custom-field {
  margin-bottom: 14px;
  border-radius: 16px;
  background: #f7f9fc;
  overflow: hidden;
}

:deep(.custom-field .van-field__label) {
  width: 64px;
  color: #455a64;
  font-weight: 500;
}

:deep(.custom-field .van-field__control) {
  color: #1f2d3d;
}

:deep(.custom-field .van-icon) {
  color: #1989fa;
  font-size: 18px;
  margin-right: 6px;
}

.agreement-row {
  margin: 6px 4px 18px;
}

.agreement-text {
  font-size: 12px;
  color: #8e9aa5;
  line-height: 1.8;
}

.btn-group {
  margin-top: 8px;
}

.submit-btn {
  height: 44px;
  font-size: 15px;
  font-weight: 600;
  border: none;
  box-shadow: 0 8px 16px rgba(25, 137, 250, 0.18);
}

.back-btn {
  margin-top: 14px;
  height: 44px;
  font-size: 15px;
  color: #1989fa;
  border-color: #b6dcff;
  background: #f8fbff;
}
</style>