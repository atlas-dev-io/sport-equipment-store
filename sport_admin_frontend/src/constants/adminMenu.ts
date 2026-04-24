import type { Component } from 'vue'
import {
  GridOutline,
  CubeOutline,
  ReceiptOutline,
  PeopleOutline,
  ArchiveOutline,
} from '@vicons/ionicons5'

export interface AdminMenuItem {
  label: string
  key: string
  icon: Component
  roles: Array<'merchant' | 'admin'>
}

export const adminMenuList: AdminMenuItem[] = [
  {
    label: '后台首页',
    key: '/admin/dashboard',
    icon: GridOutline,
    roles: ['merchant', 'admin'],
  },
  {
    label: '商品管理',
    key: '/admin/products',
    icon: CubeOutline,
    roles: ['merchant', 'admin'],
  },
  {
    label: '库存管理',
    key: '/admin/inventory',
    icon: ArchiveOutline,
    roles: ['merchant', 'admin'],
  },
  {
    label: '订单管理',
    key: '/admin/orders',
    icon: ReceiptOutline,
    roles: ['merchant', 'admin'],
  },
  {
    label: '用户管理',
    key: '/admin/users',
    icon: PeopleOutline,
    roles: ['admin'],
  },
]