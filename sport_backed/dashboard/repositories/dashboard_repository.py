from decimal import Decimal

from django.db.models import Count, Sum

from orders.models import Order, OrderItem
from products.models import Product


class DashboardRepository:
    SALE_STATUS_LIST = ["paid", "shipped", "completed"]

    @staticmethod
    def get_user_role(user):
        profile = getattr(user, "profile", None)
        return profile.role if profile else ""

    @staticmethod
    def get_product_queryset(user, role):
        if role == "admin":
            return Product.objects.all()
        return Product.objects.filter(merchant=user)

    @staticmethod
    def get_order_queryset(user, role):
        if role == "admin":
            return Order.objects.all()

        return Order.objects.filter(
            items__product__merchant=user
        ).distinct()

    @staticmethod
    def get_order_item_queryset(user, role):
        if role == "admin":
            return OrderItem.objects.select_related(
                "order", "product", "product__category"
            )

        return OrderItem.objects.select_related(
            "order", "product", "product__category"
        ).filter(
            product__merchant=user
        )

    @staticmethod
    def get_status_distribution(order_queryset):
        return list(
            order_queryset.values("status").annotate(
                count=Count("id", distinct=True)
            ).order_by()
        )

    @staticmethod
    def get_category_sales_ranking(order_item_queryset, limit=8):
        return list(
            order_item_queryset.filter(
                order__status__in=DashboardRepository.SALE_STATUS_LIST
            ).values(
                "product__category__name"
            ).annotate(
                sales_quantity=Sum("quantity"),
                sales_amount=Sum("subtotal_amount"),
            ).order_by("-sales_amount", "-sales_quantity")[:limit]
        )

    @staticmethod
    def get_admin_sales_amount(order_queryset):
        return order_queryset.filter(
            status__in=DashboardRepository.SALE_STATUS_LIST
        ).aggregate(
            total=Sum("pay_amount")
        )["total"] or Decimal("0.00")

    @staticmethod
    def get_merchant_sales_amount(order_item_queryset):
        return order_item_queryset.filter(
            order__status__in=DashboardRepository.SALE_STATUS_LIST
        ).aggregate(
            total=Sum("subtotal_amount")
        )["total"] or Decimal("0.00")