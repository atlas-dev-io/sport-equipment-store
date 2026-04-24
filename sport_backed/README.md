# Sport Backend

[English](./README_EN.md) | 简体中文

![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-REST-red)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)

`sport_backed` 是运动装备销售系统的后端服务，负责提供用户、商品、购物车、订单、支付、推荐和管理看板等 API。

## 技术栈

- `Django`
- `Django REST Framework`
- `PyMySQL`
- `django-cors-headers`
- `drf-yasg`

## 目录结构

```text
sport_backed/
├─ users/       # 用户、资料、商家申请、后台用户管理
├─ products/    # 商品、分类、库存与库存日志
├─ cart/        # 购物车
├─ orders/      # 订单、订单状态流转
├─ payments/    # 模拟支付
├─ recommend/   # 浏览记录、收藏、推荐
├─ dashboard/   # 管理端统计与图表数据
├─ sport_backed/# 项目配置
├─ manage.py
└─ requirements.txt
```

## 核心模块

- `users`：注册、登录、当前用户、个人信息、收货信息、商家申请
- `products`：商品列表、详情、创建编辑、库存调整、库存预警
- `cart`：购物车查询、加购、修改数量、删除、清空
- `orders`：创建订单、订单详情、支付、取消、发货、完成、退款
- `payments`：模拟支付记录
- `recommend`：浏览记录、收藏状态、推荐商品
- `dashboard`：管理端统计概览和图表数据

## API 路由

```text
/api/users/
/api/products/
/api/cart/
/api/orders/
/api/payments/
/api/dashboard/
/api/recommend/
```

## 本地运行

### 环境准备

- Python 3.11+
- MySQL 8+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 数据库迁移与启动

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 配置说明

默认数据库配置写在：

```text
sport_backed/settings.py
```

当前项目默认使用 MySQL，本地运行前请先确保数据库已创建并且账号可用。

## 当前实现说明

- 认证方式当前为 Token 认证。
- 支付流程当前为模拟支付。
- 推荐流程当前为规则版推荐。
- `tests.py` 已预留，但自动化测试仍可继续补充。

## 相关文档

- 仓库主页：[../README.md](../README.md)
- 用户端：[../sport_user_frontend/README.md](../sport_user_frontend/README.md)
- 管理端：[../sport_admin_frontend/README.md](../sport_admin_frontend/README.md)

## License

本模块遵循仓库根目录中的 [MIT License](../LICENSE)。
