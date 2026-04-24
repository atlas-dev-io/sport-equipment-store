from django.db.models import Prefetch

from cart.models import CartItem
from orders.models import Order, OrderItem
from products.models import InventoryLog, Product


class OrderRepository:
    """
    订单仓库层
    """

    @staticmethod
    def get_checked_cart_items(user):
        return (
            CartItem.objects
            .select_related("cart", "product", "product__category")
            .filter(cart__user=user, checked=True)
            .order_by("id")
        )

    @staticmethod
    def get_products_for_update(product_ids):
        return Product.objects.select_for_update().filter(id__in=product_ids)

    @staticmethod
    def create_order(**kwargs):
        return Order.objects.create(**kwargs)

    @staticmethod
    def create_order_item(**kwargs):
        return OrderItem.objects.create(**kwargs)

    @staticmethod
    def save_product(product):
        product.save()
        return product

    @staticmethod
    def create_inventory_log(**kwargs):
        return InventoryLog.objects.create(**kwargs)

    @staticmethod
    def delete_cart_items(cart_item_ids):
        CartItem.objects.filter(id__in=cart_item_ids).delete()

    @staticmethod
    def get_order_detail(order_id, user):
        return (
            Order.objects
            .prefetch_related(
                Prefetch("items", queryset=OrderItem.objects.order_by("id"))
            )
            .filter(id=order_id, user=user)
            .first()
        )