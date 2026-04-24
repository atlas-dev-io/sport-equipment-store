from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.serializers.order_status_serializer import (
    MockPayOrderSerializer,
    OrderStatusActionSerializer,
    OrderStatusResultSerializer,
    ShipOrderSerializer,
)
from orders.services.order_status_service import OrderStatusService


class PayOrderController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = MockPayOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = OrderStatusService.pay_order(
                user=request.user,
                order_id=id,
                method=serializer.validated_data["method"],
            )
            data = OrderStatusResultSerializer(order).data
            return Response(
                {"code": 200, "message": "支付成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"code": 400, "message": str(e), "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"code": 403, "message": str(e), "data": None}, status=status.HTTP_403_FORBIDDEN)


class CancelOrderController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = OrderStatusActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = OrderStatusService.cancel_order(
                user=request.user,
                order_id=id,
                remark=serializer.validated_data.get("remark", ""),
            )
            data = OrderStatusResultSerializer(order).data
            return Response(
                {"code": 200, "message": "取消订单成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"code": 400, "message": str(e), "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"code": 403, "message": str(e), "data": None}, status=status.HTTP_403_FORBIDDEN)


class ShipOrderController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = ShipOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = OrderStatusService.ship_order(
                user=request.user,
                order_id=id,
                shipping_company=serializer.validated_data["shipping_company"],
                tracking_no=serializer.validated_data["tracking_no"],
                shipping_remark=serializer.validated_data.get("shipping_remark", ""),
            )
            data = OrderStatusResultSerializer(order).data
            return Response(
                {"code": 200, "message": "订单发货成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"code": 400, "message": str(e), "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"code": 403, "message": str(e), "data": None}, status=status.HTTP_403_FORBIDDEN)


class CompleteOrderController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = OrderStatusActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = OrderStatusService.complete_order(
                user=request.user,
                order_id=id,
                remark=serializer.validated_data.get("remark", ""),
            )
            data = OrderStatusResultSerializer(order).data
            return Response(
                {"code": 200, "message": "订单完成成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"code": 400, "message": str(e), "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"code": 403, "message": str(e), "data": None}, status=status.HTTP_403_FORBIDDEN)


class RefundOrderController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = OrderStatusActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = OrderStatusService.refund_order(
                user=request.user,
                order_id=id,
                remark=serializer.validated_data.get("remark", ""),
            )
            data = OrderStatusResultSerializer(order).data
            return Response(
                {"code": 200, "message": "订单退款成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"code": 400, "message": str(e), "data": None}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"code": 403, "message": str(e), "data": None}, status=status.HTTP_403_FORBIDDEN)