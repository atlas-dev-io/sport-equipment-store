<template>
  <div class="login-page">
    <div class="top-bg"></div>

    <div class="login-card">
      <div class="brand-area">
        <div class="logo-box">运</div>
        <h1 class="title">运动装备销售系统</h1>
        <p class="subtitle">精选装备，便捷下单，开启你的运动生活</p>
      </div>

      <div class="form-area">
        <van-field
          v-model="form.username"
          class="custom-field"
          name="username"
          label="账号"
          placeholder="请输入用户名或手机号"
          clearable
        >
          <template #left-icon>
            <van-icon name="contact-o" />
          </template>
        </van-field>

        <van-field
          v-model="form.password"
          class="custom-field"
          type="password"
          name="password"
          label="密码"
          placeholder="请输入登录密码"
          clearable
          @keyup.enter="onLogin"
        >
          <template #left-icon>
            <van-icon name="lock" />
          </template>
        </van-field>

        <div class="options-row">
          <span class="remember-text">登录后可查看购物车和订单</span>
          <span class="forget-text">忘记密码？</span>
        </div>

        <div class="btn-group">
          <van-button
            type="primary"
            block
            round
            class="login-btn"
            :loading="loading"
            @click="onLogin"
          >
            立即登录
          </van-button>

          <van-button
            plain
            block
            round
            class="register-btn"
            @click="goRegister"
          >
            去注册
          </van-button>
        </div>
      </div>
    </div>

    <div class="bottom-tip">
      登录即表示你已阅读并同意
      <span>《用户协议》</span>
      与
      <span>《隐私政策》</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showFailToast, showSuccessToast } from 'vant'
import { handleLogin } from '@/api/auth'

const router = useRouter()
const route = useRoute()

const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
})

function goRegister() {
  router.push('/register')
}

async function onLogin() {
  if (!form.username.trim()) {
    showFailToast('请输入账号')
    return
  }

  if (!form.password.trim()) {
    showFailToast('请输入密码')
    return
  }

  try {
    loading.value = true

    await handleLogin({
      username: form.username.trim(),
      password: form.password,
    })

    showSuccessToast('登录成功')

    const redirect = typeof route.query.redirect === 'string'
      ? route.query.redirect
      : '/'

    router.replace(redirect)
  } catch (error: any) {
    const message =
      error?.response?.data?.message ||
      error?.response?.data?.detail ||
      '登录失败，请检查账号或密码'
    showFailToast(message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #eaf6ff 0%, #f7fbff 38%, #f5f7fa 100%);
  position: relative;
  overflow: hidden;
}

.top-bg {
  height: 180px;
  background: linear-gradient(135deg, #1989fa 0%, #4fc3f7 100%);
  border-bottom-left-radius: 28px;
  border-bottom-right-radius: 28px;
  box-shadow: 0 8px 24px rgba(25, 137, 250, 0.18);
}

.login-card {
  width: calc(100% - 32px);
  margin: -92px auto 0;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(21, 101, 192, 0.08);
  padding: 28px 18px 24px;
  box-sizing: border-box;
}

.brand-area {
  text-align: center;
  margin-bottom: 22px;
}

.logo-box {
  width: 64px;
  height: 64px;
  margin: 0 auto 14px;
  border-radius: 20px;
  background: linear-gradient(135deg, #1989fa 0%, #5ad8ff 100%);
  color: #fff;
  font-size: 30px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 18px rgba(25, 137, 250, 0.22);
}

.title {
  margin: 0;
  font-size: 24px;
  color: #1f2d3d;
  font-weight: 700;
}

.subtitle {
  margin: 10px 0 0;
  color: #7a8a99;
  font-size: 13px;
  line-height: 1.6;
}

.form-area {
  margin-top: 8px;
}

.custom-field {
  margin-bottom: 14px;
  border-radius: 16px;
  background: #f7f9fc;
  overflow: hidden;
}

:deep(.custom-field .van-field__label) {
  width: 52px;
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

.options-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 4px 4px 18px;
  font-size: 13px;
}

.remember-text {
  color: #8a97a5;
}

.forget-text {
  color: #1989fa;
  font-weight: 500;
}

.btn-group {
  margin-top: 8px;
}

.login-btn {
  height: 44px;
  font-size: 15px;
  font-weight: 600;
  border: none;
  box-shadow: 0 8px 16px rgba(25, 137, 250, 0.2);
}

.register-btn {
  margin-top: 14px;
  height: 44px;
  font-size: 15px;
  color: #1989fa;
  border-color: #b6dcff;
  background: #f8fbff;
}

.bottom-tip {
  width: calc(100% - 48px);
  margin: 22px auto 0;
  text-align: center;
  color: #98a4af;
  font-size: 12px;
  line-height: 1.8;
}

.bottom-tip span {
  color: #1989fa;
}
</style>