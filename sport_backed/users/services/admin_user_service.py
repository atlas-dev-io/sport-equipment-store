from django.contrib.auth import get_user_model

from users.repositories.user_repository import UserRepository

User = get_user_model()


class AdminUserService:
    @staticmethod
    def _get_user_role(user):
        profile = getattr(user, "profile", None)
        return profile.role if profile else ""

    @staticmethod
    def check_admin_permission(user):
        role = AdminUserService._get_user_role(user)
        if role != "admin":
            raise ValueError("当前账号无权访问用户管理")

    @staticmethod
    def get_user_list(request_user, keyword="", role="", is_active=""):
        AdminUserService.check_admin_permission(request_user)

        queryset = User.objects.select_related("profile").all().order_by("-id")

        if keyword:
            keyword = keyword.strip()
            queryset = queryset.filter(username__icontains=keyword)

        if role:
            queryset = queryset.filter(profile__role=role)

        if is_active in ["true", "false", "True", "False", "1", "0"]:
            active_value = str(is_active).lower() in ["true", "1"]
            queryset = queryset.filter(is_active=active_value)

        return queryset

    @staticmethod
    def update_user(request_user, target_user, data):
        AdminUserService.check_admin_permission(request_user)

        profile = UserRepository.get_or_create_user_profile(target_user)

        if "role" in data:
            profile.role = data["role"]

        if "nickname" in data:
            profile.nickname = data["nickname"].strip()

        if "phone" in data:
            profile.phone = data["phone"].strip()

        if "email" in data:
            target_user.email = data["email"].strip()

        if "is_active" in data:
            target_user.is_active = data["is_active"]

        target_user.save()
        profile.save()

        return target_user