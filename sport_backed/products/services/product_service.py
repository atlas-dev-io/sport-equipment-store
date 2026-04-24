from typing import Optional

from django.db.models import Q

from products.models import Product
from products.repositories.product_repository import ProductRepository


class ProductService:
    """
    商品服务层
    """

    @staticmethod
    def _get_user_role(user):
        profile = getattr(user, "profile", None)
        return profile.role if profile else ""

    @staticmethod
    def get_product_list(request):
        user = request.user
        role = ProductService._get_user_role(user) if user and user.is_authenticated else ""

        # 管理端：商家看自己的商品，管理员看全部商品
        if role == "merchant":
            queryset = ProductRepository.base_queryset().filter(merchant=user)
        elif role == "admin":
            queryset = ProductRepository.base_queryset()
        else:
            # 用户端：只看上架商品
            queryset = ProductRepository.public_queryset()

        category = request.query_params.get("category")
        brand = request.query_params.get("brand")
        keyword = request.query_params.get("keyword")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        is_recommend = request.query_params.get("is_recommend")
        ordering = request.query_params.get("ordering", "-id")
        status = request.query_params.get("status")

        if category:
            queryset = queryset.filter(category_id=category)

        if brand:
            queryset = queryset.filter(brand__icontains=brand.strip())

        if keyword:
            keyword = keyword.strip()
            queryset = queryset.filter(
                Q(name__icontains=keyword)
                | Q(subtitle__icontains=keyword)
                | Q(brand__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(sku__icontains=keyword)
            )

        if min_price:
            try:
                queryset = queryset.filter(price__gte=min_price)
            except Exception:
                pass

        if max_price:
            try:
                queryset = queryset.filter(price__lte=max_price)
            except Exception:
                pass

        if is_recommend in ["true", "1", "True"]:
            queryset = queryset.filter(is_recommend=True)

        if status:
            queryset = queryset.filter(status=status)

        allowed_ordering = {
            "id",
            "-id",
            "price",
            "-price",
            "sales_count",
            "-sales_count",
            "created_at",
            "-created_at",
            "stock",
            "-stock",
        }
        if ordering not in allowed_ordering:
            ordering = "-id"

        return queryset.order_by(ordering)

    @staticmethod
    def get_product_detail(product_id: int, user=None) -> Optional[Product]:
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return None

        if user and user.is_authenticated:
            role = ProductService._get_user_role(user)

            if role == "admin":
                return product

            if role == "merchant" and product.merchant_id == user.id:
                return product

        if product.status != "on_sale" or not product.category.is_active:
            return None

        return product

    @staticmethod
    def create_product(data: dict, user):
        sku = data["sku"]
        if ProductRepository.exists_by_sku(sku):
            raise ValueError("SKU已存在")

        product = ProductRepository.create_product(
            merchant=user,
            category=data["category"],
            name=data["name"],
            subtitle=data.get("subtitle", ""),
            brand=data.get("brand", ""),
            sku=sku,
            price=data["price"],
            market_price=data.get("market_price", 0),
            stock=data.get("stock", 0),
            description=data.get("description", ""),
            main_image=data.get("main_image", ""),
            status=data.get("status", "on_sale"),
            is_recommend=data.get("is_recommend", False),
        )
        return product

    @staticmethod
    def update_product(product: Product, data: dict):
        sku = data.get("sku")
        if sku and ProductRepository.exists_by_sku_exclude_self(sku, product.id):
            raise ValueError("SKU已存在")

        for field, value in data.items():
            setattr(product, field, value)

        ProductRepository.save(product)
        return product

    @staticmethod
    def delete_product(product: Product):
        ProductRepository.delete(product)
        return True