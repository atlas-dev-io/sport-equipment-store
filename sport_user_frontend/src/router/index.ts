import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import CartView from '@/views/CartView.vue'
import CheckoutView from '@/views/CheckoutView.vue'
import OrdersView from '@/views/OrdersView.vue'
import ProfileView from '@/views/ProfileView.vue'
import AddressView from '@/views/AddressView.vue'
import ProfileInfoView from '@/views/ProfileInfoView.vue'
import FavoriteView from '@/views/FavoriteView.vue'
import BrowseHistoryView from '@/views/BrowseHistoryView.vue'
import RecommendView from '@/views/RecommendView.vue'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: '首页 - 运动装备商城' },
    },
    {
      path: '/product/:id',
      name: 'product-detail',
      component: ProductDetailView,
      meta: { title: '商品详情 - 运动装备商城' },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { title: '登录 - 运动装备商城' },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { title: '注册 - 运动装备商城' },
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView,
      meta: { requiresAuth: true, title: '购物车 - 运动装备商城' },
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: CheckoutView,
      meta: { requiresAuth: true, title: '提交订单 - 运动装备商城' },
    },
    {
      path: '/orders',
      name: 'orders',
      component: OrdersView,
      meta: { requiresAuth: true, title: '我的订单 - 运动装备商城' },
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true, title: '我的 - 运动装备商城' },
    },
    {
      path: '/profile/address',
      name: 'profile-address',
      component: AddressView,
      meta: { requiresAuth: true, title: '收货信息 - 运动装备商城' },
    },
    {
      path: '/profile/info',
      name: 'profile-info',
      component: ProfileInfoView,
      meta: { requiresAuth: true, title: '个人资料 - 运动装备商城' },
    },
    {
      path: '/profile/favorites',
      name: 'profile-favorites',
      component: FavoriteView,
      meta: { requiresAuth: true, title: '我的收藏 - 运动装备商城' },
    },
    {
      path: '/profile/history',
      name: 'profile-history',
      component: BrowseHistoryView,
      meta: { requiresAuth: true, title: '浏览记录 - 运动装备商城' },
    },
    {
      path: '/profile/recommend',
      name: 'profile-recommend',
      component: RecommendView,
      meta: { requiresAuth: true, title: '猜你喜欢 - 运动装备商城' },
    },
  ],
})

router.beforeEach((to) => {
  const userStore = useUserStore()

  document.title = (to.meta.title as string) || '运动装备商城'

  if (userStore.isLogin && (to.path === '/login' || to.path === '/register')) {
    return '/'
  }

  if (to.meta.requiresAuth && !userStore.isLogin) {
    return {
      path: '/login',
      query: {
        redirect: to.fullPath,
      },
    }
  }

  return true
})

export default router