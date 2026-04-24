from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers.admin_user_serializer import (
    AdminUserListSerializer,
    AdminUserUpdateSerializer,
)
from users.serializers.merchant_application_serializer import (
    MerchantApplicationReviewSerializer,
    MerchantApplicationSerializer,
)
from users.services.admin_user_service import AdminUserService
from users.services.merchant_application_service import MerchantApplicationService

User = get_user_model()


class AdminUserListController(APIView):
    """
    GET /api/users/admin/users/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        keyword = request.query_params.get("keyword", "")
        role = request.query_params.get("role", "")
        is_active = request.query_params.get("is_active", "")

        try:
            queryset = AdminUserService.get_user_list(
                request_user=request.user,
                keyword=keyword,
                role=role,
                is_active=is_active,
            )
            data = AdminUserListSerializer(queryset, many=True).data
            return Response(
                {"code": 200, "message": "获取用户列表成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 403, "message": str(e), "data": None},
                status=status.HTTP_403_FORBIDDEN,
            )


class AdminUserDetailController(APIView):
    """
    PUT /api/users/admin/users/<id>/
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            target_user = User.objects.select_related("profile").get(id=id)
        except User.DoesNotExist:
            return Response(
                {"code": 404, "message": "用户不存在", "data": None},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AdminUserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = AdminUserService.update_user(
                request_user=request.user,
                target_user=target_user,
                data=serializer.validated_data,
            )
            data = AdminUserListSerializer(user).data
            return Response(
                {"code": 200, "message": "更新用户成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 403, "message": str(e), "data": None},
                status=status.HTTP_403_FORBIDDEN,
            )


class AdminMerchantApplicationListController(APIView):
    """
    GET /api/users/admin/merchant-applications/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        keyword = request.query_params.get("keyword", "")
        status_value = request.query_params.get("status", "")

        try:
            queryset = MerchantApplicationService.get_application_list(
                request_user=request.user,
                keyword=keyword,
                status=status_value,
            )
            data = MerchantApplicationSerializer(queryset, many=True).data
            return Response(
                {"code": 200, "message": "获取商家申请列表成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 403, "message": str(e), "data": None},
                status=status.HTTP_403_FORBIDDEN,
            )


class AdminMerchantApplicationReviewController(APIView):
    """
    POST /api/users/admin/merchant-applications/<id>/review/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = MerchantApplicationReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            application = MerchantApplicationService.review_application(
                request_user=request.user,
                application_id=id,
                action=serializer.validated_data["action"],
                review_remark=serializer.validated_data.get("review_remark", ""),
            )
            data = MerchantApplicationSerializer(application).data
            return Response(
                {"code": 200, "message": "商家申请审核成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 400, "message": str(e), "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )