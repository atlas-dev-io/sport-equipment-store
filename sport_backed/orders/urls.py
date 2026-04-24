from django.urls import path

from orders.controllers.order_controller import (
    CreateOrderController,
    OrderDetailController,
    OrderListController,
)
from orders.controllers.order_status_controller import (
    CancelOrderController,
    CompleteOrderController,
    PayOrderController,
    RefundOrderController,
    ShipOrderController,
)

urlpatterns = [
    path("", OrderListController.as_view(), name="order-list"),
    path("create/", CreateOrderController.as_view(), name="order-create"),
    path("<int:id>/", OrderDetailController.as_view(), name="order-detail"),

    path("<int:id>/pay/", PayOrderController.as_view(), name="order-pay"),
    path("<int:id>/cancel/", CancelOrderController.as_view(), name="order-cancel"),
    path("<int:id>/ship/", ShipOrderController.as_view(), name="order-ship"),
    path("<int:id>/complete/", CompleteOrderController.as_view(), name="order-complete"),
    path("<int:id>/refund/", RefundOrderController.as_view(), name="order-refund"),
]