# Sport Equipment Store

[English](./README_EN.md) | 简体中文

![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)

一个基于 `Django + MySQL + Vue 3` 的运动装备销售系统，采用前后端分离架构，包含后端服务、用户端和管理端三部分。

## 项目概览

- Python 版本: `3.11.15`
- 操作系统: `Ubuntu 24.04 LTS`
- 后端：`Django + Django REST Framework`
- 数据库：`MySQL 8.0.45`
- 用户端：`Vue 3 + Vite + Vant + Pinia`
- 管理端：`Vue 3 + Vite + Naive UI + ECharts`
- 架构形态：三端协同的电商系统

## 功能特性

- 用户注册、登录、个人资料、默认收货信息
- 商品分类、商品列表、商品详情、关键词搜索
- 购物车、下单、订单状态流转
- 模拟支付、退款、发货、订单完成
- 浏览记录、收藏、规则版推荐
- 商品管理、库存管理、订单管理、用户管理
- 管理端数据看板与统计图表

## 仓库结构

```text
sport/
├─ sport_backed/          # Django 后端
├─ sport_user_frontend/   # Vue 用户端
├─ sport_admin_frontend/  # Vue 管理端
└─ README.md
```

## 快速开始

### 1. 启动后端

```bash
cd sport_backed
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 2. 启动用户端

```bash
cd sport_user_frontend
pnpm install
pnpm dev
```

### 3. 启动管理端

```bash
cd sport_admin_frontend
pnpm install
pnpm dev
```

## 模块说明

### 后端 `sport_backed`

- 用户、商家申请、权限信息
- 商品、分类、库存日志
- 购物车、订单、支付记录
- 推荐、收藏、浏览历史
- 管理端统计与看板数据接口

### 用户端 `sport_user_frontend`

- 首页商品浏览
- 商品详情
- 登录注册
- 购物车与结算
- 订单列表
- 个人中心、收藏、浏览记录、推荐

### 管理端 `sport_admin_frontend`

- 管理员/商家登录
- 商品管理
- 库存管理
- 订单管理
- 用户管理
- 数据看板

## 开发说明

- 当前支付流程为模拟支付，不接入真实支付网关。
- 当前物流流程为模拟发货与物流信息维护。
- 后端数据库配置默认写在 `sport_backed/sport_backed/settings.py`。
- 推荐模块当前为规则版 MVP，不是机器学习推荐系统。

## 文档导航

- 后端说明：[sport_backed/README.md](./sport_backed/README.md)
- 用户端说明：[sport_user_frontend/README.md](./sport_user_frontend/README.md)
- 管理端说明：[sport_admin_frontend/README.md](./sport_admin_frontend/README.md)

## 路线图

- [x] 三端基础架构搭建
- [x] 电商核心流程打通
- [x] 用户端与管理端页面实现
- [x] 推荐与看板模块接入
- [ ] 测试与部署文档进一步完善
- [ ] 配置文件环境变量化

## License

本项目采用 [MIT License](./LICENSE)。
