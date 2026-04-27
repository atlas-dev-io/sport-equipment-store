# Sport Backend

[简体中文](./README.md) | English

![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-REST-red)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)

`sport_backed` is the backend service for the sport equipment store. It provides APIs for users, products, cart, orders, payments, recommendations, and dashboard analytics.

## Tech Stack

- `Django`
- `Django REST Framework`
- `djangorestframework-simplejwt`
- `PyMySQL`
- `python-dotenv`
- `django-cors-headers`
- `drf-yasg`

## Structure

```text
sport_backed/
├─ users/       # users, profiles, merchant applications, admin user management
├─ products/    # products, categories, inventory, inventory logs
├─ cart/        # shopping cart
├─ orders/      # orders and order status flow
├─ payments/    # mock payment
├─ recommend/   # browse history, favorites, recommendations
├─ dashboard/   # admin dashboard analytics
├─ sport_backed/# project settings
├─ .env.example # environment variable example
├─ manage.py
└─ requirements.txt
```

## Core Modules

- `users`: register, login, current user, profile, shipping info, merchant application
- `products`: list, detail, create/update, inventory adjustment, warning threshold
- `cart`: query cart, add item, update quantity, remove item, clear cart
- `orders`: create order, order detail, pay, cancel, ship, complete, refund
- `payments`: mock payment records
- `recommend`: browse history, favorite status, recommended products
- `dashboard`: overview metrics and chart data for the admin client

## API Prefixes

```text
/api/users/
/api/products/
/api/cart/
/api/orders/
/api/payments/
/api/dashboard/
/api/recommend/
```

## Local Development

### Requirements

- Python 3.11+
- MySQL 8+
- The existing `sport` conda environment is the recommended local environment

### Install

```bash
pip install -r requirements.txt
```

### Migrate and Run

```bash
cp .env.example .env
# update DJANGO_SECRET_KEY and DB_* values as needed
python manage.py migrate
python manage.py runserver
```

## Configuration Notes

Runtime configuration is loaded from:

```text
sport_backed/.env
```

The default variables include `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.

The project expects a working local MySQL database before startup. When you run `python manage.py test` without explicitly setting `DB_ENGINE`, the test suite automatically falls back to SQLite.

## Implementation Notes

- Authentication now uses JWT, and authenticated requests should send `Authorization: Bearer <access_token>`.
- The register and login APIs return both `token` (access token) and `refresh_token`.
- Logout immediately revokes the current access token and blacklists the user's issued refresh tokens.
- Payments are mock payments only.
- Recommendations are currently rule-based.
- Automated auth coverage now includes register, login, current-user lookup, and post-logout token revocation.

## Related Docs

- Repository root: [../README_EN.md](../README_EN.md)
- User client: [../sport_user_frontend/README_EN.md](../sport_user_frontend/README_EN.md)
- Admin client: [../sport_admin_frontend/README_EN.md](../sport_admin_frontend/README_EN.md)

## License

This module follows the [MIT License](../LICENSE) defined at the repository root.
