# Sport Admin Frontend

[English](./README_EN.md) | 简体中文

![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js&logoColor=white)
![Naive UI](https://img.shields.io/badge/Naive_UI-Admin-18A058)
![ECharts](https://img.shields.io/badge/ECharts-6-AA344D)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)

`sport_admin_frontend` 是运动装备销售系统的管理端，面向管理员和商家，提供商品、库存、订单、用户和数据看板等后台能力。

## 技术栈

- `Vue 3`
- `Vite`
- `Vue Router`
- `Pinia`
- `Axios`
- `Naive UI`
- `ECharts`

## 功能模块

- 管理端登录
- 数据看板
- 商品管理
- 库存管理与库存日志
- 订单管理
- 用户管理
- 商家申请审核

## 目录结构

```text
src/
├─ api/              # 接口封装
├─ components/       # 公共组件
├─ constants/        # 常量配置
├─ layouts/          # 管理端布局
├─ router/           # 路由与权限控制
├─ stores/           # Pinia 状态管理
├─ views/            # 页面视图
├─ App.vue
└─ main.ts
```

## 本地运行

### 安装依赖

```bash
pnpm install
```

### 开发模式

```bash
pnpm dev
```

### 生产构建

```bash
pnpm build
```

### 代码检查

```bash
pnpm lint
```

## 页面说明

- `AdminLoginView.vue`：登录页
- `DashboardView.vue`：统计看板
- `ProductManageView.vue`：商品管理
- `InventoryManageView.vue`：库存管理
- `OrderManageView.vue`：订单管理
- `UserManageView.vue`：用户与商家申请审核
- `ForbiddenView.vue`：权限不足提示页

## 权限说明

- `admin`：可访问完整后台功能
- `merchant`：可访问商品、库存、订单、看板
- 非授权用户：跳转到登录页或 `403`

> 建议先导入 `../sport_backed/sql/seed_demo_data.sql`，再使用管理端账号登录。

## 当前实现说明

- 登录后会把后端返回的 access token 保存在本地，并在接口请求中携带 `Authorization: Bearer <token>`。
- 演示商家账号：`merchant_power`、`merchant_yoga`、`merchant_outdoor`，默认密码 `123456`。
- 演示管理员账号：`admin_ops`、`admin_supply`、`admin_super`，默认密码 `123456`。
- 发货、退款等业务依赖后端订单接口。
- 图表使用 `ECharts` 渲染。
- 页面以桌面端管理系统交互为主。
- 当前仍保留少量脚手架默认页面，可继续精简。

## 相关文档

- 仓库主页：[../README.md](../README.md)
- 后端说明：[../sport_backed/README.md](../sport_backed/README.md)
- 用户端说明：[../sport_user_frontend/README.md](../sport_user_frontend/README.md)

## License

本模块遵循仓库根目录中的 [MIT License](../LICENSE)。
