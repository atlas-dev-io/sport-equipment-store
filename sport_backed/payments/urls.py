from django.urls import path

from payments.controllers.payment_controller import (
    MockPaymentController,
    PaymentByOrderController,
    PaymentDetailController,
)

urlpatterns = [
    path("mock/pay/", MockPaymentController.as_view(), name="mock-payment"),
    path("order/<int:order_id>/", PaymentByOrderController.as_view(), name="payment-by-order"),
    path("<int:id>/", PaymentDetailController.as_view(), name="payment-detail"),
]