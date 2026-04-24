
```text
src/
├─ api/                    # 所有接口
│  ├─ auth.ts
│  ├─ product.ts
│  ├─ cart.ts
│  ├─ order.ts
│  └─ request.ts
│
├─ assets/                 # 静态资源
│
├─ components/             # 公共组件
│  ├─ business/            # 业务公共组件
│  │  ├─ ProductCard.vue
│  │  ├─ CartItemCard.vue
│  │  └─ OrderCard.vue
│  └─ common/              # 通用组件
│     ├─ AppHeader.vue
│     ├─ EmptyState.vue
│     └─ LoadingView.vue
│
├─ layouts/                # 布局
│  └─ UserTabLayout.vue    # 底部 tab 主布局
│
├─ router/
│  └─ index.ts
│
├─ stores/
│  ├─ user.ts
│  ├─ cart.ts
│  └─ app.ts
│
├─ utils/
│  ├─ storage.ts
│  ├─ auth.ts
│  ├─ price.ts
│  └─ guards.ts
│
├─ views/
│  ├─ auth/
│  │  ├─ LoginView.vue
│  │  └─ RegisterView.vue
│  │
│  ├─ home/
│  │  └─ HomeView.vue          # 商品列表/首页
│  │
│  ├─ product/
│  │  └─ ProductDetailView.vue
│  │
│  ├─ cart/
│  │  └─ CartView.vue
│  │
│  ├─ order/
│  │  ├─ CreateOrderView.vue
│  │  ├─ OrderListView.vue
│  │  └─ OrderDetailView.vue
│  │
│  ├─ profile/
│  │  └─ ProfileView.vue
│  │
│  └─ not-found/
│     └─ NotFoundView.vue
│
├─ App.vue
└─ main.ts

```