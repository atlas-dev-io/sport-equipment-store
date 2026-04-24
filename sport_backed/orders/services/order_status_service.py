import random

from django.db import transaction
from django.utils import timezone

from orders.repositories.order_status_repository import OrderStatusRepository


class OrderStatusService:
    """
    订单状态服务层
    """

    @staticmethod
    def _get_user_role(user):
        profile = getattr(user, "profile", None)
        return profile.role if profile else ""

    @staticmethod
    def _check_owner_or_admin(user, order):
        role = OrderStatusService._get_user_role(user)
        if order.user_id != user.id and role != "admin":
            raise PermissionError("无权操作该订单")

    @staticmethod
    def _check_merchant_or_admin(user):
        role = OrderStatusService._get_user_role(user)
        if role not in ["merchant", "admin"]:
            raise PermissionError("仅商家或管理员可执行该操作")

    @staticmethod
    def _generate_payment_no(user_id: int) -> str:
        now_str = timezone.now().strftime("%Y%m%d%H%M%S")
        rand_str = str(random.randint(1000, 9999))
        return f"PAY{now_str}{user_id}{rand_str}"

    @staticmethod
    def _rollback_inventory_and_sales(order, operator=None, remark_prefix="订单回滚恢复库存"):
        items = list(order.items.all())
        product_ids = [item.product_id for item in items if item.product_id]

        locked_products = OrderStatusRepository.get_products_for_update(product_ids)
        product_map = {product.id: product for product in locked_products}

        for item in items:
            if not item.product_id:
                continue

            product = product_map.get(item.product_id)
            if not product:
                continue

            before_stock = product.stock
            product.stock += item.quantity
            product.sales_count = max(0, product.sales_count - item.quantity)
            OrderStatusRepository.save_product(product)

            OrderStatusRepository.create_inventory_log(
                product=product,
                change_type="increase",
                change_quantity=item.quantity,
                before_stock=before_stock,
                after_stock=product.stock,
                remark=f"{remark_prefix}：{order.order_no}",
                operator=operator,
            )

    @staticmethod
    @transaction.atomic
    def pay_order(user, order_id: int, method: str = "mock"):
        order = OrderStatusRepository.get_order_for_update(order_id)
        if not order:
            raise ValueError("订单不存在")

        OrderStatusService._check_owner_or_admin(user, order)

        if order.status != "pending_payment":
            raise ValueError("只有待支付订单才能支付")

        payment = OrderStatusRepository.get_payment_by_order(order)
        if not payment:
            payment = OrderStatusRepository.create_payment(
                payment_no=OrderStatusService._generate_payment_no(user.id),
                order=order,
                user=order.user,
                method=method,
                status="success",
                amount=order.pay_amount,
                paid_at=timezone.now(),
                remark="模拟支付成功",
            )
        else:
            payment.method = method
            payment.status = "success"
            payment.amount = order.pay_amount
            payment.paid_at = timezone.now()
            payment.remark = "模拟支付成功"
            OrderStatusRepository.save_payment(payment)

        order.status = "paid"
        order.paid_at = timezone.now()
        OrderStatusRepository.save_order(order)

        return OrderStatusRepository.get_order_detail(order.id)

    @staticmethod
    @transaction.atomic
    def cancel_order(user, order_id: int, remark: str = ""):
        order = OrderStatusRepository.get_order_for_update(order_id)
        if not order:
            raise ValueError("订单不存在")

        OrderStatusService._check_owner_or_admin(user, order)

        if order.status != "pending_payment":
            raise ValueError("只有待支付订单才能取消")

        OrderStatusService._rollback_inventory_and_sales(
            order=order,
            operator=user,
            remark_prefix="取消订单恢复库存",
        )

        order.status = "canceled"
        if remark:
            order.remark = remark
        OrderStatusRepository.save_order(order)

        return OrderStatusRepository.get_order_detail(order.id)

    @staticmethod
    @transaction.atomic
    def ship_order(user, order_id: int, remark: str = ""):
        order = OrderStatusRepository.get_order_for_update(order_id)
        if not order:
            raise ValueError("订单不存在")

        OrderStatusService._check_merchant_or_admin(user)

        if order.status != "paid":
            raise ValueError("只有已支付订单才能发货")

        order.status = "shipped"
        order.shipped_at = timezone.now()
        if remark:
            order.remark = remark
        OrderStatusRepository.save_order(order)

        return OrderStatusRepository.get_order_detail(order.id)

    @staticmethod
    @transaction.atomic
    def complete_order(user, order_id: int, remark: str = ""):
        order = OrderStatusRepository.get_order_for_update(order_id)
        if not order:
            raise ValueError("订单不存在")

        OrderStatusService._check_owner_or_admin(user, order)

        if order.status != "shipped":
            raise ValueError("只有已发货订单才能完成")

        order.status = "completed"
        order.completed_at = timezone.now()
        if remark:
            order.remark = remark
        OrderStatusRepository.save_order(order)

        return OrderStatusRepository.get_order_detail(order.id)

    @staticmethod
    @transaction.atomic
    def refund_order(user, order_id: int, remark: str = ""):
        order = OrderStatusRepository.get_order_for_update(order_id)
        if not order:
            raise ValueError("订单不存在")

        OrderStatusService._check_merchant_or_admin(user)

        if order.status != "paid":
            raise ValueError("只有已支付订单才能退款")

        OrderStatusService._rollback_inventory_and_sales(
            order=order,
            operator=user,
            remark_prefix="订单退款恢复库存",
        )

        payment = OrderStatusRepository.get_payment_by_order(order)
        if payment:
            payment.status = "refunded"
            payment.remark = remark or "订单退款成功"
            OrderStatusRepository.save_payment(payment)

        order.status = "refunded"
        if remark:
            order.remark = remark
        OrderStatusRepository.save_order(order)

        return OrderStatusRepository.get_order_detail(order.id)