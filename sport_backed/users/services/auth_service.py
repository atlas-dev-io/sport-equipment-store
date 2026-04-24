from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.authtoken.models import Token

from users.repositories.user_repository import UserRepository


class AuthService:
    """
    认证服务层
    """

    @staticmethod
    @transaction.atomic
    def register(data: dict):
        username = data["username"]
        password = data["password"]
        email = data.get("email", "").strip()
        nickname = data.get("nickname", "").strip()
        phone = data.get("phone", "").strip()
        role = data.get("role", "customer")

        if UserRepository.exists_by_username(username):
            raise ValueError("用户名已存在")

        if email and UserRepository.exists_by_email(email):
            raise ValueError("邮箱已被注册")

        user = UserRepository.create_user(
            username=username,
            password=password,
            email=email,
        )
        UserRepository.create_user_profile(
            user=user,
            role=role,
            nickname=nickname,
            phone=phone,
        )
        token, _ = Token.objects.get_or_create(user=user)

        return {
            "user_id": user.id,
            "username": user.username,
            "token": token.key,
        }

    @staticmethod
    def login(username: str, password: str):
        user = authenticate(username=username, password=password)
        if not user:
            raise ValueError("用户名或密码错误")

        if not user.is_active:
            raise ValueError("用户已被禁用")

        token, _ = Token.objects.get_or_create(user=user)

        return {
            "user_id": user.id,
            "username": user.username,
            "token": token.key,
        }

    @staticmethod
    def get_current_user(user_id: int):
        user = UserRepository.get_user_with_profile(user_id)
        if not user:
            raise ValueError("用户不存在")

        profile = getattr(user, "profile", None)
        latest_application = UserRepository.get_latest_merchant_application(user)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email or "",
            "is_active": user.is_active,
            "date_joined": user.date_joined,

            "role": profile.role if profile else "",
            "nickname": profile.nickname if profile else "",
            "phone": profile.phone if profile else "",
            "avatar": profile.avatar if profile else "",
            "gender": profile.gender if profile else "",
            "birthday": profile.birthday if profile else None,
            "address": profile.address if profile else "",

            "merchant_application_status": latest_application.status if latest_application else "",
            "merchant_application_shop_name": latest_application.shop_name if latest_application else "",
            "merchant_application_review_remark": latest_application.review_remark if latest_application else "",
        }

    @staticmethod
    def logout(user):
        Token.objects.filter(user=user).delete()
        return True