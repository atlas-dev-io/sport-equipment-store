from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from orders.serializers.order_serializer import (
    CreateOrderSerializer,
    OrderDetailSerializer,
)
from orders.services.order_service import OrderService


def get_user_role(user):
    profile = getattr(user, "profile", None)
    return profile.role if profile else ""


class OrderListController(APIView):
    """
    GET /api/orders/
    用户端：看自己的订单
    商家端：看自己商品相关订单
    管理员：看全部订单
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = get_user_role(request.user)
        status_param = request.query_params.get("status", "").strip()

        if role == "admin":
            orders = Order.objects.prefetch_related("items", "items__product", "items__product__merchant").select_related("user").all()
        elif role == "merchant":
            orders = Order.objects.prefetch_related("items", "items__product", "items__product__merchant").select_related("user").filter(
                items__product__merchant=request.user
            ).distinct()
        else:
            orders = Order.objects.prefetch_related("items", "items__product", "items__product__merchant").select_related("user").filter(
                user=request.user
            )

        if status_param:
            orders = orders.filter(status=status_param)

        orders = orders.order_by("-created_at")
        data = OrderDetailSerializer(orders, many=True).data

        return Response(
            {
                "code": 200,
                "message": "获取订单列表成功",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class CreateOrderController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = OrderService.create_order_from_cart(
                user=request.user,
                data=serializer.validated_data,
            )
            data = OrderDetailSerializer(order).data
            return Response(
                {
                    "code": 200,
                    "message": "创建订单成功",
                    "data": data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response(
                {
                    "code": 400,
                    "message": str(e),
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class OrderDetailController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        role = get_user_role(request.user)

        try:
            order = Order.objects.prefetch_related("items", "items__product", "items__product__merchant").select_related("user").get(id=id)
        except Order.DoesNotExist:
            return Response(
                {
                    "code": 404,
                    "message": "订单不存在",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if role == "admin":
            pass
        elif role == "merchant":
            if not order.items.filter(product__merchant=request.user).exists():
                return Response(
                    {"code": 403, "message": "无权查看该订单", "data": None},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            if order.user_id != request.user.id:
                return Response(
                    {"code": 403, "message": "无权查看该订单", "data": None},
                    status=status.HTTP_403_FORBIDDEN,
                )

        data = OrderDetailSerializer(order).data
        return Response(
            {
                "code": 200,
                "message": "获取订单详情成功",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )