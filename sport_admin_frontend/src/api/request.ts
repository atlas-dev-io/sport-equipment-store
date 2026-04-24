import axios, { type InternalAxiosRequestConfig, type AxiosError } from 'axios'
import router from '@/router'
import { useAdminUserStore } from '@/stores/adminUser'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 10000,
})

request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const adminUserStore = useAdminUserStore()
    const token = adminUserStore.token

    if (token) {
      config.headers.Authorization = `Token ${token}`
    }

    return config
  },
  (error: AxiosError) => Promise.reject(error),
)

request.interceptors.response.use(
  (response) => response.data,
  async (error: AxiosError) => {
    const adminUserStore = useAdminUserStore()
    const status = error.response?.status
    const currentRoute = router.currentRoute.value

    if (status === 401) {
      adminUserStore.logout()

      if (currentRoute.path !== '/login') {
        await router.replace({
          path: '/login',
          query: {
            redirect: currentRoute.fullPath,
          },
        })
      }
    }

    return Promise.reject(error)
  },
)

export default request