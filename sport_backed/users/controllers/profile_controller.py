from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers.profile_info_serializer import (
    MerchantApplicationCreateSerializer,
    ProfileInfoSerializer,
    UpdateProfileInfoSerializer,
)
from users.serializers.profile_serializer import (
    ShippingInfoSerializer,
    UpdateShippingInfoSerializer,
)
from users.serializers.merchant_application_serializer import MerchantApplicationSerializer
from users.services.profile_service import ProfileService
from users.services.merchant_application_service import MerchantApplicationService


class ShippingInfoController(APIView):
    """
    收货信息
    GET /api/users/profile/shipping/
    PUT /api/users/profile/shipping/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            result = ProfileService.get_shipping_info(request.user.id)
            serializer = ShippingInfoSerializer(result)
            return Response(
                {"code": 200, "message": "获取收货信息成功", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 404, "message": str(e), "data": None},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request):
        serializer = UpdateShippingInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = ProfileService.update_shipping_info(
                request.user.id,
                serializer.validated_data,
            )
            response_serializer = ShippingInfoSerializer(result)
            return Response(
                {"code": 200, "message": "保存收货信息成功", "data": response_serializer.data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 400, "message": str(e), "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileInfoController(APIView):
    """
    个人资料
    GET /api/users/profile/info/
    PUT /api/users/profile/info/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            result = ProfileService.get_profile_info(request.user.id)
            serializer = ProfileInfoSerializer(result)
            return Response(
                {"code": 200, "message": "获取个人资料成功", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 404, "message": str(e), "data": None},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request):
        serializer = UpdateProfileInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = ProfileService.update_profile_info(
                request.user.id,
                serializer.validated_data,
            )
            response_serializer = ProfileInfoSerializer(result)
            return Response(
                {"code": 200, "message": "保存个人资料成功", "data": response_serializer.data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 400, "message": str(e), "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BecomeMerchantController(APIView):
    """
    提交商家申请
    POST /api/users/profile/become-merchant/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MerchantApplicationCreateSerializer(data=request.data or {})
        serializer.is_valid(raise_exception=True)

        try:
            application = MerchantApplicationService.submit_application(
                request.user.id,
                serializer.validated_data,
            )
            data = MerchantApplicationSerializer(application).data
            return Response(
                {"code": 200, "message": "商家申请已提交，请等待管理员审核", "data": data},
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {"code": 400, "message": str(e), "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )