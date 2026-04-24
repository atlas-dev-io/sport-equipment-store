from django.contrib.auth import get_user_model

from users.models import MerchantApplication, UserProfile

User = get_user_model()


class UserRepository:
    """
    用户仓库层
    """

    @staticmethod
    def exists_by_username(username: str) -> bool:
        return User.objects.filter(username=username).exists()

    @staticmethod
    def exists_by_email(email: str) -> bool:
        if not email:
            return False
        return User.objects.filter(email=email).exists()

    @staticmethod
    def create_user(username: str, password: str, email: str = ""):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

    @staticmethod
    def create_user_profile(user, role="customer", nickname="", phone=""):
        return UserProfile.objects.create(
            user=user,
            role=role,
            nickname=nickname,
            phone=phone,
        )

    @staticmethod
    def get_user_with_profile(user_id: int):
        return User.objects.select_related("profile").filter(id=user_id).first()

    @staticmethod
    def get_user_by_username(username: str):
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_or_create_user_profile(user):
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    @staticmethod
    def get_latest_merchant_application(user):
        return MerchantApplication.objects.filter(user=user).order_by("-id").first()

    @staticmethod
    def get_pending_merchant_application(user):
        return MerchantApplication.objects.filter(
            user=user,
            status="pending",
        ).order_by("-id").first()

    @staticmethod
    def create_merchant_application(**kwargs):
        return MerchantApplication.objects.create(**kwargs)

    @staticmethod
    def merchant_application_queryset():
        return MerchantApplication.objects.select_related("user", "reviewed_by").all()

    @staticmethod
    def get_merchant_application_by_id(application_id: int):
        return MerchantApplication.objects.select_related("user", "reviewed_by").filter(id=application_id).first()

    @staticmethod
    def save_merchant_application(application):
        application.save()
        return application