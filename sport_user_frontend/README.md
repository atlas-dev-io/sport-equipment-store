# Sport User Frontend

[English](./README_EN.md) | 简体中文

![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js&logoColor=white)
![Vant](https://img.shields.io/badge/Vant-4-1989FA)
![Pinia](https://img.shields.io/badge/Pinia-Store-FFD859)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)

`sport_user_frontend` 是运动装备销售系统的用户端，面向普通消费者，提供商品浏览、购物车、下单、订单管理和个人中心等功能。

## 技术栈

- `Vue 3`
- `Vite`
- `Vue Router`
- `Pinia`
- `Axios`
- `Vant`

## 功能模块

- 首页商品列表与搜索
- 商品详情页
- 用户注册与登录
- 购物车管理
- 提交订单与订单列表
- 个人中心
- 收货信息维护
- 收藏、浏览记录、猜你喜欢

## 目录结构

```text
src/
├─ api/          # 接口封装
├─ assets/       # 静态资源
├─ router/       # 路由配置
├─ stores/       # Pinia 状态管理
├─ views/        # 页面视图
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

- `HomeView.vue`：首页与商品列表
- `ProductDetailView.vue`：商品详情
- `CartView.vue`：购物车
- `CheckoutView.vue`：提交订单
- `OrdersView.vue`：订单列表
- `ProfileView.vue`：个人中心
- `FavoriteView.vue`：收藏列表
- `BrowseHistoryView.vue`：浏览记录
- `RecommendView.vue`：猜你喜欢

> 请先启动 `sport_backed`，再启动当前前端项目。

> 如果需要可直接登录的演示数据，可先导入 `../sport_backed/sql/seed_demo_data.sql`。

## 当前实现说明

- 当前项目更偏移动端 H5 体验。
- 登录后会把后端返回的 access token 保存在本地，并在接口请求中携带 `Authorization: Bearer <token>`。
- 演示普通用户账号：`customer_chen`、`customer_li`、`customer_wang`，默认密码均为 `123456`。
- 支付流程为模拟支付。
- 推荐模块为规则版推荐。
- 代码中保留了少量脚手架页面，可按需要继续清理。

## 相关文档

- 仓库主页：[../README.md](../README.md)
- 后端说明：[../sport_backed/README.md](../sport_backed/README.md)
- 管理端说明：[../sport_admin_frontend/README.md](../sport_admin_frontend/README.md)

## License

本模块遵循仓库根目录中的 [MIT License](../LICENSE)。
