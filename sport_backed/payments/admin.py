from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "payment_no",
        "order",
        "user",
        "method",
        "status",
        "amount",
        "paid_at",
        "created_at",
    )
    search_fields = ("payment_no", "order__order_no", "user__username")
    list_filter = ("method", "status", "created_at")