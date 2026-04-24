<template>
  <div class="login-page">
    <div
      class="left-section"
      @mousemove="handleMouseMove"
      @mouseleave="resetEyes"
    >
      <div class="logo-area">
        <div class="logo">
          <n-icon size="26">
            <LayersOutline />
          </n-icon>
          <span>运动商城管理后台</span>
        </div>
      </div>

      <div class="illustration-wrap">
        <div class="character-scene">
          <div class="char purple">
            <span class="eye eye-left">
              <span class="pupil" :style="pupilStyle"></span>
            </span>
            <span class="eye eye-right">
              <span class="pupil" :style="pupilStyle"></span>
            </span>
          </div>

          <div class="char black">
            <span class="eye eye-left">
              <span class="pupil" :style="pupilStyle"></span>
            </span>
            <span class="eye eye-right">
              <span class="pupil" :style="pupilStyle"></span>
            </span>
          </div>

          <div class="char orange">
            <span class="eye eye-left">
              <span class="pupil" :style="pupilStyle"></span>
            </span>
            <span class="eye eye-right">
              <span class="pupil" :style="pupilStyle"></span>
            </span>
          </div>

          <div class="char yellow">
            <span class="eye eye-left">
              <span class="pupil" :style="pupilStyle"></span>
            </span>
            <span class="eye eye-right">
              <span class="pupil" :style="pupilStyle"></span>
            </span>
            <span class="mouth"></span>
          </div>
        </div>
      </div>

      <div class="footer-links">
        <button class="link-btn" type="button" @click="showPrivacy = true">
          隐私政策
        </button>
        <button class="link-btn" type="button" @click="showTerms = true">
          服务条款
        </button>
      </div>

      <div class="decorative-grid"></div>
      <div class="decorative-circle circle-1"></div>
      <div class="decorative-circle circle-2"></div>
    </div>

    <div class="right-section">
      <div class="login-form-container">
        <div class="mobile-logo">
          <n-icon size="24">
            <LayersOutline />
          </n-icon>
          <span>运动商城管理后台</span>
        </div>

        <div class="form-header">
          <h1>欢迎回来！</h1>
          <p>请输入您的账号信息</p>
        </div>

        <n-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-placement="top"
          class="login-form"
          @submit.prevent="handleSubmit"
        >
          <n-form-item label="用户名" path="username">
            <n-input
              v-model:value="form.username"
              placeholder="请输入用户名"
              size="large"
              clearable
            />
          </n-form-item>

          <n-form-item label="密码" path="password">
            <n-input
              v-model:value="form.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              show-password-on="mousedown"
            >
              <template #password-visible-icon>
                <n-icon>
                  <EyeOutline />
                </n-icon>
              </template>
              <template #password-invisible-icon>
                <n-icon>
                  <EyeOffOutline />
                </n-icon>
              </template>
            </n-input>
          </n-form-item>

          <n-alert
            v-if="errorText"
            type="error"
            :show-icon="false"
            class="error-alert"
          >
            {{ errorText }}
          </n-alert>

          <n-button
            type="primary"
            size="large"
            block
            :loading="submitting"
            attr-type="submit"
            class="login-btn"
          >
            登录
          </n-button>
        </n-form>
      </div>
    </div>

    <n-modal v-model:show="showPrivacy" preset="card" style="width: 720px" title="隐私政策">
      <div class="policy-content">
        <p>欢迎使用运动商城管理后台。为保障您的合法权益，请在使用本系统前认真阅读本隐私政策。</p>
        <p>1. 我们会在您登录、使用管理功能时，收集必要的账户信息，例如用户名、角色、联系方式等，用于身份识别与权限控制。</p>
        <p>2. 您在后台录入的商品、订单、库存、用户审核等业务数据，仅用于系统运营与管理，不会在未经授权的情况下向无关第三方披露。</p>
        <p>3. 我们会采取合理的技术与管理措施保护数据安全，包括权限隔离、登录鉴权、接口访问控制等。</p>
        <p>4. 如因法律法规、监管要求或司法机关要求，我们可能依法提供必要的数据配合。</p>
        <p>5. 您继续使用本系统，即视为同意本隐私政策的内容。</p>
      </div>
    </n-modal>

    <n-modal v-model:show="showTerms" preset="card" style="width: 720px" title="服务条款">
      <div class="policy-content">
        <p>欢迎使用运动商城管理后台。在使用本系统前，请仔细阅读以下服务条款。</p>
        <p>1. 本系统仅限经过授权的商家与管理员账号使用，不得将账号借予他人使用。</p>
        <p>2. 用户应妥善保管账号和密码，因账号保管不善导致的风险由账号持有人自行承担。</p>
        <p>3. 商家在后台发布商品、处理订单、管理库存时，应确保信息真实、合法、有效，不得上传违法违规内容。</p>
        <p>4. 管理员有权依据系统规则对商家申请、用户信息及业务内容进行审核、调整或限制。</p>
        <p>5. 如用户违反法律法规或平台规则，平台有权暂停或终止其使用权限。</p>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMessage, type FormInst, type FormRules } from 'naive-ui'
import { EyeOffOutline, EyeOutline, LayersOutline } from '@vicons/ionicons5'
import { handleAdminLogin } from '@/api/auth'

const router = useRouter()
const route = useRoute()
const message = useMessage()

const formRef = ref<FormInst | null>(null)
const submitting = ref(false)
const errorText = ref('')
const showPrivacy = ref(false)
const showTerms = ref(false)

const form = reactive({
  username: '',
  password: '',
})

const rules: FormRules = {
  username: [
    {
      required: true,
      message: '请输入用户名',
      trigger: ['blur', 'input'],
    },
  ],
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: ['blur', 'input'],
    },
  ],
}

const eyeOffsetX = ref(0)
const eyeOffsetY = ref(0)
const autoLookTimer = ref<number | null>(null)

const pupilStyle = computed(() => ({
  transform: `translate(${eyeOffsetX.value}px, ${eyeOffsetY.value}px)`,
}))

function handleMouseMove(event: MouseEvent) {
  const target = event.currentTarget as HTMLElement | null
  if (!target) return

  const rect = target.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2

  const dx = event.clientX - centerX
  const dy = event.clientY - centerY

  const limit = 4
  eyeOffsetX.value = Math.max(-limit, Math.min(limit, dx / 60))
  eyeOffsetY.value = Math.max(-limit, Math.min(limit, dy / 90))
}

function resetEyes() {
  eyeOffsetX.value = 0
  eyeOffsetY.value = 0
}

function startAutoLook() {
  if (autoLookTimer.value) {
    window.clearInterval(autoLookTimer.value)
  }

  autoLookTimer.value = window.setInterval(() => {
    const presets = [
      { x: 0, y: 0 },
      { x: 2, y: 0.5 },
      { x: -2, y: 0.5 },
      { x: 1.5, y: -0.5 },
      { x: -1.5, y: -0.5 },
      { x: 0.5, y: 1.2 },
    ]
    const next = presets[Math.floor(Math.random() * presets.length)]
    eyeOffsetX.value = next.x
    eyeOffsetY.value = next.y
  }, 2200)
}

async function handleSubmit() {
  errorText.value = ''

  try {
    await formRef.value?.validate()
  } catch {
    return
  }

  try {
    submitting.value = true

    await handleAdminLogin({
      username: form.username.trim(),
      password: form.password,
    })

    const redirect = (route.query.redirect as string) || '/admin/dashboard'
    message.success('登录成功')
    await router.replace(redirect)
  } catch (error: any) {
    errorText.value =
      error?.response?.data?.message ||
      error?.message ||
      error?.response?.data?.detail ||
      '登录失败，请检查用户名和密码'
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  startAutoLook()
})

onBeforeUnmount(() => {
  if (autoLookTimer.value) {
    window.clearInterval(autoLookTimer.value)
  }
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr;
  background: #fff;
}

.left-section {
  display: none;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #9ca3af 0%, #6b7280 48%, #4b5563 100%);
  color: #fff;
  padding: 44px 48px 36px;
}

.logo-area {
  position: relative;
  z-index: 2;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
}

.illustration-wrap {
  position: relative;
  z-index: 2;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.character-scene {
  position: relative;
  width: 430px;
  height: 430px;
}

.char {
  position: absolute;
  bottom: 0;
  border-radius: 22px 22px 0 0;
}

.char .eye {
  position: absolute;
  top: 48px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fff;
  overflow: hidden;
  animation: blink 5.2s infinite;
}

.pupil {
  position: absolute;
  top: 7px;
  left: 7px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #1f2937;
  transition: transform 0.18s ease;
}

.eye-left {
  left: 30px;
}

.eye-right {
  right: 30px;
}

.purple {
  left: 72px;
  width: 170px;
  height: 330px;
  background: linear-gradient(180deg, #7c4dff 0%, #5b34f4 100%);
}

.black {
  left: 230px;
  width: 86px;
  height: 245px;
  background: #242424;
  transform: rotate(-2deg);
}

.orange {
  left: 20px;
  width: 190px;
  height: 190px;
  border-radius: 95px 95px 0 0;
  background: #f79a65;
}

.yellow {
  left: 300px;
  width: 120px;
  height: 220px;
  border-radius: 60px 60px 0 0;
  background: #e4d451;
}

.yellow .mouth {
  position: absolute;
  left: 28px;
  bottom: 90px;
  width: 62px;
  height: 4px;
  border-radius: 999px;
  background: #222;
}

.footer-links {
  position: relative;
  z-index: 2;
  display: flex;
  gap: 24px;
  align-items: center;
}

.link-btn {
  padding: 0;
  border: none;
  background: transparent;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.95);
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.link-btn:hover {
  opacity: 0.8;
  text-decoration: underline;
}

.decorative-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  background-size: 20px 20px;
}

.decorative-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(50px);
}

.circle-1 {
  top: 22%;
  right: 20%;
  width: 260px;
  height: 260px;
  background: rgba(255, 255, 255, 0.08);
}

.circle-2 {
  bottom: 14%;
  left: 18%;
  width: 340px;
  height: 340px;
  background: rgba(255, 255, 255, 0.08);
}

.right-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 20px;
  background: #fff;
}

.login-form-container {
  width: 100%;
  max-width: 420px;
}

.mobile-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
  color: #111827;
  font-size: 18px;
  font-weight: 600;
}

.form-header {
  text-align: center;
  margin-bottom: 34px;
}

.form-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.form-header p {
  margin: 10px 0 0;
  font-size: 14px;
  color: #9ca3af;
}

.login-form {
  width: 100%;
}

.error-alert {
  margin-bottom: 18px;
}

.login-btn {
  margin-top: 8px;
  height: 44px;
  border-radius: 10px;
}

.policy-content {
  font-size: 14px;
  line-height: 1.9;
  color: #374151;
}

.policy-content p {
  margin: 0 0 12px;
}

:deep(.n-form-item-label__text) {
  font-size: 15px;
  font-weight: 600;
  color: #374151;
}

:deep(.n-input) {
  --n-height: 44px !important;
}

:deep(.n-input__input-el) {
  font-size: 15px;
}

@keyframes blink {
  0%,
  44%,
  48%,
  52%,
  100% {
    transform: scaleY(1);
  }
  46%,
  50% {
    transform: scaleY(0.12);
  }
}

@media (min-width: 1024px) {
  .login-page {
    grid-template-columns: 1.05fr 1fr;
  }

  .left-section {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .mobile-logo {
    display: none;
  }

  .right-section {
    padding: 48px 36px;
  }

  .login-form-container {
    max-width: 400px;
  }

  .form-header {
    margin-bottom: 38px;
  }

  .form-header h1 {
    font-size: 28px;
  }
}

@media (max-width: 1023px) {
  .right-section {
    padding: 28px 18px;
  }

  .login-form-container {
    max-width: 100%;
  }
}
</style>