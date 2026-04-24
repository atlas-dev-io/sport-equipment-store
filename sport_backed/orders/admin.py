from django.contrib import admin

from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_no",
        "user",
        "status",
        "total_amount",
        "pay_amount",
        "receiver_name",
        "receiver_phone",
        "created_at",
    )
    search_fields = ("order_no", "user__username", "receiver_name", "receiver_phone")
    list_filter = ("status", "created_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product_name",
        "product_price",
        "quantity",
        "subtotal_amount",
        "created_at",
    )
    search_fields = ("order__order_no", "product_name")