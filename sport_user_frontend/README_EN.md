# Sport User Frontend

[简体中文](./README.md) | English

![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js&logoColor=white)
![Vant](https://img.shields.io/badge/Vant-4-1989FA)
![Pinia](https://img.shields.io/badge/Pinia-Store-FFD859)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)

`sport_user_frontend` is the customer-facing application of the sport equipment store. It provides product browsing, shopping cart, checkout, order management, and profile features.

## Tech Stack

- `Vue 3`
- `Vite`
- `Vue Router`
- `Pinia`
- `Axios`
- `Vant`

## Features

- Home page product list and search
- Product detail page
- User registration and login
- Shopping cart management
- Order creation and order list
- Profile center
- Shipping info management
- Favorites, browse history, and recommendations

## Structure

```text
src/
├─ api/          # API wrappers
├─ assets/       # static assets
├─ router/       # route config
├─ stores/       # Pinia stores
├─ views/        # page views
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

- `HomeView.vue`: home page and product list
- `ProductDetailView.vue`: product detail
- `CartView.vue`: shopping cart
- `CheckoutView.vue`: checkout
- `OrdersView.vue`: orders
- `ProfileView.vue`: profile center
- `FavoriteView.vue`: favorites
- `BrowseHistoryView.vue`: browse history
- `RecommendView.vue`: recommendations

> Start `sport_backed` before running this frontend.

## Notes

- The current UX is mainly mobile-oriented.
- Payments are mock payments.
- Recommendations are rule-based.
- A few scaffold pages are still present and can be cleaned up later.

## Related Docs

- Repository root: [../README_EN.md](../README_EN.md)
- Backend docs: [../sport_backed/README_EN.md](../sport_backed/README_EN.md)
- Admin client docs: [../sport_admin_frontend/README_EN.md](../sport_admin_frontend/README_EN.md)
