import axios, {
  AxiosError,
  type AxiosInstance,
  type InternalAxiosRequestConfig,
} from 'axios'
import router from '@/router'
import { useUserStore } from '@/stores/user'

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

const request: AxiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 10000,
})

request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const userStore = useUserStore()
    const token = userStore.token

    if (token) {
      config.headers.Authorization = `Token ${token}`
    }

    return config
  },
  (error: AxiosError) => Promise.reject(error),
)

request.interceptors.response.use(
  (response) => {
    return response.data
  },
  async (error: AxiosError) => {
    const userStore = useUserStore()
    const status = error.response?.status
    const currentRoute = router.currentRoute.value

    if (status === 401) {
      userStore.logout()

      if (currentRoute.path !== '/login') {
        await router.push({
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