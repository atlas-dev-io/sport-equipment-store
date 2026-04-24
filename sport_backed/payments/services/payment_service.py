import random

from django.db import transaction
from django.utils import timezone

from payments.repositories.payment_repository import PaymentRepository


class PaymentService:
    """
    模拟支付服务层
    """

    @staticmethod
    def _get_user_role(user):
        profile = getattr(user, "profile", None)
        return profile.role if profile else ""

    @staticmethod
    def _check_owner_or_admin(user, order):
        role = PaymentService._get_user_role(user)
        if order.user_id != user.id and role != "admin":
            raise PermissionError("无权支付该订单")

    @staticmethod
    def _generate_payment_no(user_id: int) -> str:
        now_str = timezone.now().strftime("%Y%m%d%H%M%S")
        rand_str = str(random.randint(1000, 9999))
        return f"PAY{now_str}{user_id}{rand_str}"

    @staticmethod
    @transaction.atomic
    def mock_pay(user, order_id: int, method: str = "mock", remark: str = "模拟支付成功"):
        order = PaymentRepository.get_order_for_update(order_id)
        if not order:
            raise ValueError("订单不存在")

        PaymentService._check_owner_or_admin(user, order)

        if order.status != "pending_payment":
            raise ValueError("只有待支付订单才能支付")

        payment = PaymentRepository.get_payment_by_order(order)
        if not payment:
            payment = PaymentRepository.create_payment(
                payment_no=PaymentService._generate_payment_no(user.id),
                order=order,
                user=order.user,
                method=method,
                status="success",
                amount=order.pay_amount,
                paid_at=timezone.now(),
                remark=remark,
            )
        else:
            payment.method = method
            payment.status = "success"
            payment.amount = order.pay_amount
            payment.paid_at = timezone.now()
            payment.remark = remark
            PaymentRepository.save_payment(payment)

        order.status = "paid"
        order.paid_at = timezone.now()
        PaymentRepository.save_order(order)

        return payment

    @staticmethod
    def get_payment_detail(payment_id: int):
        payment = PaymentRepository.get_payment_by_id(payment_id)
        if not payment:
            raise ValueError("支付记录不存在")
        return payment

    @staticmethod
    def get_payment_by_order(order_id: int):
        payment = PaymentRepository.get_payment_by_order_id(order_id)
        if not payment:
            raise ValueError("该订单暂无支付记录")
        return payment