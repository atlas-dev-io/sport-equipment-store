import random
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from orders.repositories.order_repository import OrderRepository


class OrderService:
    """
    订单服务层
    """

    @staticmethod
    def generate_order_no(user_id: int) -> str:
        now_str = timezone.now().strftime("%Y%m%d%H%M%S")
        rand_str = str(random.randint(1000, 9999))
        return f"ORD{now_str}{user_id}{rand_str}"

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user, data: dict):
        checked_items = list(OrderRepository.get_checked_cart_items(user))

        if not checked_items:
            raise ValueError("当前没有已勾选的购物车商品，无法创建订单")

        product_ids = [item.product_id for item in checked_items]
        locked_products = OrderRepository.get_products_for_update(product_ids)
        product_map = {product.id: product for product in locked_products}

        total_amount = Decimal("0.00")
        cart_item_ids_to_delete = []

        for item in checked_items:
            product = product_map.get(item.product_id)
            if not product:
                raise ValueError(f"商品不存在：{item.product_id}")

            if product.status != "on_sale":
                raise ValueError(f"商品未上架，不能下单：{product.name}")

            if not product.category.is_active:
                raise ValueError(f"商品分类不可用，不能下单：{product.name}")

            if product.stock < item.quantity:
                raise ValueError(f"商品库存不足：{product.name}")

            total_amount += product.price * item.quantity
            cart_item_ids_to_delete.append(item.id)

        order = OrderRepository.create_order(
            order_no=OrderService.generate_order_no(user.id),
            user=user,
            status="pending_payment",
            total_amount=total_amount,
            pay_amount=total_amount,
            receiver_name=data["receiver_name"],
            receiver_phone=data["receiver_phone"],
            receiver_address=data["receiver_address"],
            remark=data.get("remark", ""),
        )

        for item in checked_items:
            product = product_map[item.product_id]
            subtotal = product.price * item.quantity

            OrderRepository.create_order_item(
                order=order,
                product=product,
                product_name=product.name,
                product_image=product.main_image,
                product_price=product.price,
                quantity=item.quantity,
                subtotal_amount=subtotal,
            )

            before_stock = product.stock
            product.stock -= item.quantity
            product.sales_count += item.quantity
            OrderRepository.save_product(product)

            OrderRepository.create_inventory_log(
                product=product,
                change_type="decrease",
                change_quantity=-item.quantity,
                before_stock=before_stock,
                after_stock=product.stock,
                remark=f"订单创建扣减库存：{order.order_no}",
                operator=user,
            )

        OrderRepository.delete_cart_items(cart_item_ids_to_delete)

        return OrderRepository.get_order_detail(order.id, user)