from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recommend.serializers.recommend_serializer import (
    BrowseHistoryItemSerializer,
    FavoriteItemSerializer,
    FavoriteStatusQuerySerializer,
    FavoriteStatusSerializer,
    ProductActionSerializer,
    RecommendProductItemSerializer,
    RecommendQuerySerializer,
)
from recommend.services.recommend_service import RecommendService


class BrowseHistoryRecordController(APIView):
    """
    记录浏览历史
    POST /api/recommend/history/record/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            history = RecommendService.record_browse_history(
                user=request.user,
                product_id=serializer.validated_data["product_id"],
            )
            data = BrowseHistoryItemSerializer(history).data
            return Response(
                {"code": 200, "message": "记录浏览历史成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 400, "message": str(e), "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BrowseHistoryListController(APIView):
    """
    浏览历史列表
    GET /api/recommend/history/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        histories = RecommendService.list_browse_histories(request.user)
        data = BrowseHistoryItemSerializer(histories, many=True).data
        return Response(
            {"code": 200, "message": "获取浏览历史成功", "data": data},
            status=status.HTTP_200_OK,
        )


class FavoriteToggleController(APIView):
    """
    收藏/取消收藏
    POST /api/recommend/favorites/toggle/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = RecommendService.toggle_favorite(
                user=request.user,
                product_id=serializer.validated_data["product_id"],
            )
            message = "收藏成功" if result["is_favorite"] else "取消收藏成功"
            data = FavoriteStatusSerializer(result).data
            return Response(
                {"code": 200, "message": message, "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 400, "message": str(e), "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FavoriteStatusController(APIView):
    """
    查询商品收藏状态
    GET /api/recommend/favorites/status/?product_id=1
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = FavoriteStatusQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = RecommendService.get_favorite_status(
            user=request.user,
            product_id=serializer.validated_data["product_id"],
        )
        data = FavoriteStatusSerializer(result).data
        return Response(
            {"code": 200, "message": "获取收藏状态成功", "data": data},
            status=status.HTTP_200_OK,
        )


class FavoriteListController(APIView):
    """
    收藏列表
    GET /api/recommend/favorites/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = RecommendService.list_favorites(request.user)
        data = FavoriteItemSerializer(favorites, many=True).data
        return Response(
            {"code": 200, "message": "获取收藏列表成功", "data": data},
            status=status.HTTP_200_OK,
        )


class RecommendProductListController(APIView):
    """
    推荐商品列表
    GET /api/recommend/products/?limit=6
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RecommendQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = RecommendService.get_recommend_products(
            user=request.user,
            limit=serializer.validated_data["limit"],
        )
        data = RecommendProductItemSerializer(result, many=True).data
        return Response(
            {"code": 200, "message": "获取推荐商品成功", "data": data},
            status=status.HTTP_200_OK,
        )