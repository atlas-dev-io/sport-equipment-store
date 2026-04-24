from orders.models import Order
from payments.models import Payment


class PaymentRepository:
    """
    支付仓库层
    """

    @staticmethod
    def get_order_for_update(order_id: int):
        return (
            Order.objects
            .select_for_update()
            .select_related("user")
            .filter(id=order_id)
            .first()
        )

    @staticmethod
    def save_order(order: Order):
        order.save()
        return order

    @staticmethod
    def get_payment_by_order(order):
        return Payment.objects.filter(order=order).first()

    @staticmethod
    def create_payment(**kwargs):
        return Payment.objects.create(**kwargs)

    @staticmethod
    def save_payment(payment: Payment):
        payment.save()
        return payment

    @staticmethod
    def get_payment_by_id(payment_id: int):
        return Payment.objects.select_related("order", "user").filter(id=payment_id).first()

    @staticmethod
    def get_payment_by_order_id(order_id: int):
        return Payment.objects.select_related("order", "user").filter(order_id=order_id).first()