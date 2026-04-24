# Sport Equipment Store

[简体中文](./README.md) | English

![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)

A sport equipment e-commerce system built with `Django + MySQL + Vue 3`, using a separated frontend/backend architecture with three parts: backend service, user client, and admin client.

## Overview

- Python version: `3.11.15`
- System: `Ubuntu 24.04 LTS`
- Backend: `Django + Django REST Framework`
- Database: `MySQL 8.0.45`
- User Client: `Vue 3 + Vite + Vant + Pinia`
- Admin Client: `Vue 3 + Vite + Naive UI + ECharts`
- Architecture: three coordinated applications in one repository

## Features

- User registration, login, profile, and default shipping info
- Product categories, product listing, product detail, keyword search
- Shopping cart, checkout, and order status flow
- Mock payment, refund, shipping, and order completion
- Browse history, favorites, and rule-based recommendations
- Product management, inventory management, order management, user management
- Admin dashboard and analytics charts

## Repository Structure

```text
sport/
├─ sport_backed/          # Django backend
├─ sport_user_frontend/   # Vue user client
├─ sport_admin_frontend/  # Vue admin client
└─ README.md
```

## Quick Start

### 1. Start the backend

```bash
cd sport_backed
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


### 2. Start the user client

```bash
cd sport_user_frontend
pnpm install
pnpm dev
```

### 3. Start the admin client

```bash
cd sport_admin_frontend
pnpm install
pnpm dev
```

## Modules

### Backend `sport_backed`

- Users, merchant applications, and role information
- Products, categories, and inventory logs
- Cart, orders, and payment records
- Recommendations, favorites, and browse history
- Dashboard analytics APIs for the admin client

### User Client `sport_user_frontend`

- Home and product browsing
- Product detail
- Login and registration
- Cart and checkout
- Order list
- Profile, favorites, browse history, recommendations

### Admin Client `sport_admin_frontend`

- Admin/merchant login
- Product management
- Inventory management
- Order management
- User management
- Dashboard and charts

## Development Notes

- Payments are mock payments only.
- Logistics are simulated shipping/info management only.
- The database configuration is currently defined in `sport_backed/sport_backed/settings.py`.
- The recommendation module is currently a rule-based MVP instead of a machine-learning recommender.

## Documentation

- Backend docs: [sport_backed/README_EN.md](./sport_backed/README_EN.md)
- User client docs: [sport_user_frontend/README_EN.md](./sport_user_frontend/README_EN.md)
- Admin client docs: [sport_admin_frontend/README_EN.md](./sport_admin_frontend/README_EN.md)

## Roadmap

- [x] Three-application architecture
- [x] Core e-commerce workflow
- [x] User and admin interfaces
- [x] Recommendation and dashboard modules
- [ ] Better testing and deployment docs
- [ ] Environment-based configuration

## License

This project is licensed under the [MIT License](./LICENSE).
