from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from products.models import Category, Product
from products.permissions.product_permission import IsMerchantOrAdminOrReadOnly
from products.serializers.product_serializer import (
    CategorySimpleSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductWriteSerializer,
)
from products.services.product_service import ProductService


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class CategoryListController(generics.ListAPIView):
    """
    分类列表
    GET /api/products/categories/
    """
    serializer_class = CategorySimpleSerializer
    queryset = Category.objects.filter(is_active=True).order_by("sort_order", "id")


class ProductListCreateController(generics.ListCreateAPIView):
    """
    GET  /api/products/
    POST /api/products/
    """
    permission_classes = [IsMerchantOrAdminOrReadOnly]
    pagination_class = ProductPagination

    def get_queryset(self):
        return ProductService.get_product_list(self.request)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductWriteSerializer
        return ProductListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = ProductListSerializer(page, many=True)

        return self.get_paginated_response({
            "code": 200,
            "message": "获取商品列表成功",
            "data": serializer.data,
        })

    def create(self, request, *args, **kwargs):
        serializer = ProductWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            product = ProductService.create_product(serializer.validated_data, request.user)
            data = ProductDetailSerializer(product).data
            return Response(
                {
                    "code": 200,
                    "message": "创建商品成功",
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


class ProductRetrieveUpdateDestroyController(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("category", "merchant").prefetch_related("images").all()
    permission_classes = [IsMerchantOrAdminOrReadOnly]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ProductWriteSerializer
        return ProductDetailSerializer

    def get_object(self):
        obj = super().get_object()

        if self.request.method == "GET":
            product = ProductService.get_product_detail(obj.id, self.request.user)
            if not product:
                from django.http import Http404
                raise Http404("商品不存在")
            return product

        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductDetailSerializer(product)
        return Response(
            {
                "code": 200,
                "message": "获取商品详情成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        partial = kwargs.pop("partial", False)

        serializer = ProductWriteSerializer(product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            product = ProductService.update_product(product, serializer.validated_data)
            data = ProductDetailSerializer(product).data
            return Response(
                {
                    "code": 200,
                    "message": "更新商品成功",
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

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        ProductService.delete_product(product)
        return Response(
            {
                "code": 200,
                "message": "删除商品成功",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )