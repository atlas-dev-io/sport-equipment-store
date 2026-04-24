from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.serializers.inventory_serializer import (
    InventoryAdjustSerializer,
    InventoryLogListSerializer,
    InventoryProductListSerializer,
    InventoryWarningUpdateSerializer,
)
from products.services.inventory_service import InventoryService


class InventoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class InventoryProductListController(generics.ListAPIView):
    """
    GET /api/products/inventory/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = InventoryProductListSerializer
    pagination_class = InventoryPagination

    def get_queryset(self):
        keyword = self.request.query_params.get("keyword", "")
        low_stock_only = self.request.query_params.get("low_stock_only") in ["1", "true", "True"]
        status_value = self.request.query_params.get("status", "")
        return InventoryService.get_inventory_list(
            user=self.request.user,
            keyword=keyword,
            low_stock_only=low_stock_only,
            status=status_value,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response({
            "code": 200,
            "message": "获取库存商品列表成功",
            "data": serializer.data,
        })


class InventoryAdjustController(APIView):
    """
    POST /api/products/inventory/<id>/adjust/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = InventoryAdjustSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            product = InventoryService.adjust_inventory(
                user=request.user,
                product_id=id,
                change_type=serializer.validated_data["change_type"],
                quantity=serializer.validated_data["quantity"],
                remark=serializer.validated_data.get("remark", ""),
            )
            data = InventoryProductListSerializer(product).data
            return Response(
                {
                    "code": 200,
                    "message": "库存调整成功",
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


class InventoryWarningUpdateController(APIView):
    """
    PATCH /api/products/inventory/<id>/warning/
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        serializer = InventoryWarningUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            product = InventoryService.update_low_stock_warning(
                user=request.user,
                product_id=id,
                low_stock_warning=serializer.validated_data["low_stock_warning"],
            )
            data = InventoryProductListSerializer(product).data
            return Response(
                {
                    "code": 200,
                    "message": "低库存预警值更新成功",
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


class InventoryLogListController(generics.ListAPIView):
    """
    GET /api/products/inventory/logs/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = InventoryLogListSerializer
    pagination_class = InventoryPagination

    def get_queryset(self):
        product_id = self.request.query_params.get("product_id")
        keyword = self.request.query_params.get("keyword", "")

        if product_id:
            try:
                product_id = int(product_id)
            except Exception:
                product_id = None
        else:
            product_id = None

        return InventoryService.get_inventory_log_list(
            user=self.request.user,
            product_id=product_id,
            keyword=keyword,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response({
            "code": 200,
            "message": "获取库存日志列表成功",
            "data": serializer.data,
        })