from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.serializers.cart_serializer import (
    AddCartItemSerializer,
    CartDetailSerializer,
    CartItemSerializer,
    UpdateCartItemSerializer,
)
from cart.services.cart_service import CartService


class CartDetailController(APIView):
    """
    查看购物车
    GET /api/cart/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = CartService.get_cart_detail(request.user)
        serializer = CartDetailSerializer(cart)
        return Response(
            {
                "code": 200,
                "message": "获取购物车成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AddCartItemController(APIView):
    """
    加入购物车
    POST /api/cart/items/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart_item, created = CartService.add_to_cart(
                user=request.user,
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"],
            )
            data = CartItemSerializer(cart_item).data
            return Response(
                {
                    "code": 200,
                    "message": "加入购物车成功" if created else "购物车数量已更新",
                    "data": data,
                },
                status=status.HTTP_200_OK,
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


class CartItemUpdateDeleteController(APIView):
    """
    修改/删除购物车项
    PATCH  /api/cart/items/{id}/
    DELETE /api/cart/items/{id}/
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart_item = CartService.update_cart_item(
                user=request.user,
                item_id=id,
                data=serializer.validated_data,
            )
            data = CartItemSerializer(cart_item).data
            return Response(
                {
                    "code": 200,
                    "message": "更新购物车项成功",
                    "data": data,
                },
                status=status.HTTP_200_OK,
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
        except PermissionError as e:
            return Response(
                {
                    "code": 403,
                    "message": str(e),
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def delete(self, request, id):
        try:
            CartService.delete_cart_item(
                user=request.user,
                item_id=id,
            )
            return Response(
                {
                    "code": 200,
                    "message": "删除购物车项成功",
                    "data": None,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {
                    "code": 404,
                    "message": str(e),
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionError as e:
            return Response(
                {
                    "code": 403,
                    "message": str(e),
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )


class CartClearController(APIView):
    """
    清空购物车
    POST /api/cart/clear/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        CartService.clear_cart(request.user)
        return Response(
            {
                "code": 200,
                "message": "清空购物车成功",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )