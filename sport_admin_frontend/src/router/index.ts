import { createRouter, createWebHistory } from 'vue-router'
import { useAdminUserStore } from '@/stores/adminUser'
import AdminLayout from '@/layouts/AdminLayout.vue'
import AdminLoginView from '@/views/auth/AdminLoginView.vue'
import DashboardView from '@/views/admin/DashboardView.vue'
import ProductManageView from '@/views/admin/ProductManageView.vue'
import OrderManageView from '@/views/admin/OrderManageView.vue'
import InventoryManageView from '@/views/admin/InventoryManageView.vue'
import UserManageView from '@/views/admin/UserManageView.vue'
import ForbiddenView from '@/views/error/ForbiddenView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'admin-login',
      component: AdminLoginView,
      meta: {
        title: '管理端登录 - 运动装备商城',
        public: true,
      },
    },
    {
      path: '/403',
      name: 'forbidden',
      component: ForbiddenView,
      meta: {
        title: '无权限 - 运动装备商城管理端',
        public: true,
      },
    },
    {
      path: '/admin',
      component: AdminLayout,
      meta: {
        requiresAuth: true,
        roles: ['merchant', 'admin'],
        title: '管理端 - 运动装备商城',
      },
      children: [
        {
          path: '',
          redirect: '/admin/dashboard',
        },
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: DashboardView,
          meta: {
            title: '后台首页 - 运动装备商城管理端',
            requiresAuth: true,
            roles: ['merchant', 'admin'],
          },
        },
        {
          path: 'products',
          name: 'admin-products',
          component: ProductManageView,
          meta: {
            title: '商品管理 - 运动装备商城管理端',
            requiresAuth: true,
            roles: ['merchant', 'admin'],
          },
        },
        {
          path: 'inventory',
          name: 'admin-inventory',
          component: InventoryManageView,
          meta: {
            title: '库存管理 - 运动装备商城管理端',
            requiresAuth: true,
            roles: ['merchant', 'admin'],
          },
        },
        {
          path: 'orders',
          name: 'admin-orders',
          component: OrderManageView,
          meta: {
            title: '订单管理 - 运动装备商城管理端',
            requiresAuth: true,
            roles: ['merchant', 'admin'],
          },
        },
        {
          path: 'users',
          name: 'admin-users',
          component: UserManageView,
          meta: {
            title: '用户管理 - 运动装备商城管理端',
            requiresAuth: true,
            roles: ['admin'],
          },
        },
      ],
    },
    {
      path: '/',
      redirect: '/login',
    },
  ],
})

router.beforeEach((to) => {
  const adminUserStore = useAdminUserStore()

  document.title = (to.meta.title as string) || '运动装备商城管理端'

  if (adminUserStore.isLogin && to.path === '/login') {
    return '/admin/dashboard'
  }

  if (to.meta.requiresAuth && !adminUserStore.isLogin) {
    return {
      path: '/login',
      query: {
        redirect: to.fullPath,
      },
    }
  }

  const allowRoles = to.meta.roles as string[] | undefined
  if (allowRoles && allowRoles.length > 0) {
    if (!allowRoles.includes(adminUserStore.role)) {
      return '/403'
    }
  }

  return true
})

export default router