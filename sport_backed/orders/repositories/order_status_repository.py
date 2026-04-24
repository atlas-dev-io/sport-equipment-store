from orders.models import Order
from payments.models import Payment
from products.models import InventoryLog, Product


class OrderStatusRepository:
    """
    订单状态仓库层
    """

    @staticmethod
    def get_order_with_items(order_id: int):
        return (
            Order.objects
            .select_related("user")
            .prefetch_related("items")
            .filter(id=order_id)
            .first()
        )

    @staticmethod
    def get_order_for_update(order_id: int):
        return (
            Order.objects
            .select_for_update()
            .select_related("user")
            .prefetch_related("items")
            .filter(id=order_id)
            .first()
        )

    @staticmethod
    def get_products_for_update(product_ids):
        return Product.objects.select_for_update().filter(id__in=product_ids)

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
    def save_product(product: Product):
        product.save()
        return product

    @staticmethod
    def create_inventory_log(**kwargs):
        return InventoryLog.objects.create(**kwargs)

    @staticmethod
    def get_order_detail(order_id: int):
        return (
            Order.objects
            .select_related("user")
            .prefetch_related("items")
            .filter(id=order_id)
            .first()
        )