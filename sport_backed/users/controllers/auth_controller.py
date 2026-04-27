from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers.auth_serializer import (
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)
from users.services.auth_service import AuthService

class RegisterController(APIView):
    """
    注册接口
    POST /api/users/auth/register/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = AuthService.register(serializer.validated_data)
            return Response(
                {
                    "code": 200,
                    "message": "注册成功",
                    "data": result,
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


class LoginController(APIView):
    """
    登录接口
    POST /api/users/auth/login/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = AuthService.login(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            return Response(
                {
                    "code": 200,
                    "message": "登录成功",
                    "data": result,
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


class CurrentUserController(APIView):
    """
    获取当前登录用户信息
    GET /api/users/auth/me/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            result = AuthService.get_current_user(request.user.id)
            serializer = UserProfileSerializer(result)
            return Response(
                {
                    "code": 200,
                    "message": "获取当前用户成功",
                    "data": serializer.data,
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


class LogoutController(APIView):
    """
    退出登录
    POST /api/users/auth/logout/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        AuthService.logout(request.user, request.auth)
        return Response(
            {
                "code": 200,
                "message": "退出登录成功",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )
