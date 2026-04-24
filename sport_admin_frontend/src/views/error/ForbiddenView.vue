<template>
  <div class="forbidden-page">
    <n-result
      status="403"
      title="403 无权限"
      description="当前账号没有权限访问该页面"
    >
      <template #footer>
        <n-button type="primary" @click="goDashboard">返回后台首页</n-button>
      </template>
    </n-result>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goDashboard() {
  router.push('/admin/dashboard')
}
</script>

<style scoped>
.forbidden-page {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>