# Sport Backend

[简体中文](./README.md) | English

![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-REST-red)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)

`sport_backed` is the backend service for the sport equipment store. It provides APIs for users, products, cart, orders, payments, recommendations, and dashboard analytics.

## Tech Stack

- `Django`
- `Django REST Framework`
- `PyMySQL`
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

### Install

```bash
pip install -r requirements.txt
```

### Migrate and Run

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Configuration Notes

The default database configuration is currently defined in:

```text
sport_backed/settings.py
```

The project expects a working local MySQL database before startup.

## Implementation Notes

- Authentication currently uses token auth.
- Payments are mock payments only.
- Recommendations are currently rule-based.
- `tests.py` files are present and can be expanded with automated tests.

## Related Docs

- Repository root: [../README_EN.md](../README_EN.md)
- User client: [../sport_user_frontend/README_EN.md](../sport_user_frontend/README_EN.md)
- Admin client: [../sport_admin_frontend/README_EN.md](../sport_admin_frontend/README_EN.md)
