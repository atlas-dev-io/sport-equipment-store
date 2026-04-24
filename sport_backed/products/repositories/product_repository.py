from django.db.models import QuerySet

from products.models import Product


class ProductRepository:
    """
    商品仓库层
    负责商品数据查询与持久化
    """

    @staticmethod
    def base_queryset() -> QuerySet:
        return Product.objects.select_related("category", "merchant").prefetch_related("images").all()

    @staticmethod
    def public_queryset() -> QuerySet:
        return Product.objects.select_related("category", "merchant").prefetch_related("images").filter(
            status="on_sale",
            category__is_active=True,
        )

    @staticmethod
    def get_by_id(product_id: int):
        return Product.objects.select_related("category", "merchant").prefetch_related("images").filter(id=product_id).first()

    @staticmethod
    def create_product(**kwargs):
        return Product.objects.create(**kwargs)

    @staticmethod
    def save(product: Product):
        product.save()
        return product

    @staticmethod
    def delete(product: Product):
        product.delete()

    @staticmethod
    def exists_by_sku(sku: str) -> bool:
        return Product.objects.filter(sku=sku).exists()

    @staticmethod
    def exists_by_sku_exclude_self(sku: str, product_id: int) -> bool:
        return Product.objects.filter(sku=sku).exclude(id=product_id).exists()