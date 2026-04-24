from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.serializers.payment_serializer import (
    MockPaymentCreateSerializer,
    PaymentDetailSerializer,
)
from payments.services.payment_service import PaymentService


class MockPaymentController(APIView):
    """
    模拟支付
    POST /api/payments/mock/pay/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MockPaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payment = PaymentService.mock_pay(
                user=request.user,
                order_id=serializer.validated_data["order_id"],
                method=serializer.validated_data["method"],
                remark=serializer.validated_data.get("remark", "模拟支付成功"),
            )
            data = PaymentDetailSerializer(payment).data
            return Response(
                {
                    "code": 200,
                    "message": "模拟支付成功",
                    "data": data,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 400, "message": str(e), "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PermissionError as e:
            return Response(
                {"code": 403, "message": str(e), "data": None},
                status=status.HTTP_403_FORBIDDEN,
            )


class PaymentDetailController(APIView):
    """
    支付详情
    GET /api/payments/<id>/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            payment = PaymentService.get_payment_detail(id)
            data = PaymentDetailSerializer(payment).data
            return Response(
                {
                    "code": 200,
                    "message": "获取支付详情成功",
                    "data": data,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 404, "message": str(e), "data": None},
                status=status.HTTP_404_NOT_FOUND,
            )


class PaymentByOrderController(APIView):
    """
    按订单查看支付记录
    GET /api/payments/order/<order_id>/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            payment = PaymentService.get_payment_by_order(order_id)
            data = PaymentDetailSerializer(payment).data
            return Response(
                {
                    "code": 200,
                    "message": "获取订单支付记录成功",
                    "data": data,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 404, "message": str(e), "data": None},
                status=status.HTTP_404_NOT_FOUND,
            )