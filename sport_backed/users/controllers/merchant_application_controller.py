from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers.merchant_application_serializer import (
    AdminMerchantApplicationListSerializer,
    MerchantApplicationReviewSerializer,
)
from users.services.merchant_application_service import MerchantApplicationService


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
            data = AdminMerchantApplicationListSerializer(queryset, many=True).data
            return Response(
                {"code": 200, "message": "获取商家申请列表成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 403, "message": str(e), "data": None},
                status=status.HTTP_403_FORBIDDEN,
            )


class AdminMerchantApplicationApproveController(APIView):
    """
    POST /api/users/admin/merchant-applications/<id>/approve/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = MerchantApplicationReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            instance = MerchantApplicationService.approve_application(
                request_user=request.user,
                application_id=id,
                review_remark=serializer.validated_data.get("review_remark", ""),
            )
            data = AdminMerchantApplicationListSerializer(instance).data
            return Response(
                {"code": 200, "message": "审核通过成功", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 400, "message": str(e), "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AdminMerchantApplicationRejectController(APIView):
    """
    POST /api/users/admin/merchant-applications/<id>/reject/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = MerchantApplicationReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            instance = MerchantApplicationService.reject_application(
                request_user=request.user,
                application_id=id,
                review_remark=serializer.validated_data.get("review_remark", ""),
            )
            data = AdminMerchantApplicationListSerializer(instance).data
            return Response(
                {"code": 200, "message": "已拒绝该申请", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 400, "message": str(e), "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )