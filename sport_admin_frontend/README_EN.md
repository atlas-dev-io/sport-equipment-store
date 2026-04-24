# Sport Admin Frontend

[简体中文](./README.md) | English

![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js&logoColor=white)
![Naive UI](https://img.shields.io/badge/Naive_UI-Admin-18A058)
![ECharts](https://img.shields.io/badge/ECharts-6-AA344D)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)

`sport_admin_frontend` is the admin application for the sport equipment store. It is used by administrators and merchants to manage products, inventory, orders, users, and dashboard analytics.

## Tech Stack

- `Vue 3`
- `Vite`
- `Vue Router`
- `Pinia`
- `Axios`
- `Naive UI`
- `ECharts`

## Features

- Admin login
- Dashboard analytics
- Product management
- Inventory management and logs
- Order management
- User management
- Merchant application review

## Structure

```text
src/
├─ api/              # API wrappers
├─ components/       # shared components
├─ constants/        # constants
├─ layouts/          # admin layouts
├─ router/           # routes and access control
├─ stores/           # Pinia stores
├─ views/            # page views
├─ App.vue
└─ main.ts
```

## Local Development

### Install dependencies

```bash
pnpm install
```

### Start dev server

```bash
pnpm dev
```

### Build for production

```bash
pnpm build
```

### Lint

```bash
pnpm lint
```

## Main Views

- `AdminLoginView.vue`: login page
- `DashboardView.vue`: analytics dashboard
- `ProductManageView.vue`: product management
- `InventoryManageView.vue`: inventory management
- `OrderManageView.vue`: order management
- `UserManageView.vue`: user management and merchant review
- `ForbiddenView.vue`: access denied page

## Role Notes

- `admin`: full access to the admin system
- `merchant`: access to products, inventory, orders, and dashboard
- unauthorized users: redirected to login or `403`

## Notes

- Shipping and refund actions depend on backend order APIs.
- Charts are rendered with `ECharts`.
- The interface is primarily desktop-oriented.
- A few scaffold pages still remain and can be removed later.

## Related Docs

- Repository root: [../README_EN.md](../README_EN.md)
- Backend docs: [../sport_backed/README_EN.md](../sport_backed/README_EN.md)
- User client docs: [../sport_user_frontend/README_EN.md](../sport_user_frontend/README_EN.md)

## License

This module follows the [MIT License](../LICENSE) defined at the repository root.
