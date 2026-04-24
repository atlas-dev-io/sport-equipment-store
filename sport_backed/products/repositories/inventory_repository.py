from django.db.models import F

from products.models import InventoryLog, Product


class InventoryRepository:
    """
    库存仓库层
    """

    @staticmethod
    def _get_user_role(user):
        profile = getattr(user, "profile", None)
        return profile.role if profile else ""

    @staticmethod
    def product_queryset_by_role(user):
        role = InventoryRepository._get_user_role(user)

        queryset = Product.objects.select_related("category", "merchant").all()
        if role == "admin":
            return queryset
        return queryset.filter(merchant=user)

    @staticmethod
    def inventory_log_queryset_by_role(user):
        role = InventoryRepository._get_user_role(user)

        queryset = InventoryLog.objects.select_related("product", "product__category", "product__merchant", "operator").all()
        if role == "admin":
            return queryset
        return queryset.filter(product__merchant=user)

    @staticmethod
    def get_product_for_update(user, product_id: int):
        role = InventoryRepository._get_user_role(user)

        queryset = Product.objects.select_for_update().select_related("category", "merchant")
        if role == "admin":
            return queryset.filter(id=product_id).first()
        return queryset.filter(id=product_id, merchant=user).first()

    @staticmethod
    def save_product(product: Product):
        product.save()
        return product

    @staticmethod
    def create_inventory_log(**kwargs):
        return InventoryLog.objects.create(**kwargs)

    @staticmethod
    def filter_inventory_queryset(queryset, keyword="", low_stock_only=False, status=""):
        if keyword:
            keyword = keyword.strip()
            queryset = queryset.filter(
                name__icontains=keyword
            ) | queryset.filter(
                sku__icontains=keyword
            ) | queryset.filter(
                brand__icontains=keyword
            )

        if status:
            queryset = queryset.filter(status=status)

        if low_stock_only:
            queryset = queryset.filter(stock__lte=F("low_stock_warning"))

        return queryset.order_by("-updated_at", "-id")

    @staticmethod
    def filter_inventory_log_queryset(queryset, product_id=None, keyword=""):
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        if keyword:
            keyword = keyword.strip()
            queryset = queryset.filter(product__name__icontains=keyword) | queryset.filter(product__sku__icontains=keyword)

        return queryset.order_by("-id")