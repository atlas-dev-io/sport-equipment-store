from users.models import UserRoleChoices
from users.repositories.user_repository import UserRepository


class ProfileService:
    """
    个人中心/收货信息/个人资料服务层
    """

    @staticmethod
    def get_shipping_info(user_id: int):
        user = UserRepository.get_user_with_profile(user_id)
        if not user:
            raise ValueError("用户不存在")

        profile = getattr(user, "profile", None)
        if not profile:
            raise ValueError("用户资料不存在")

        return {
            "receiver_name": profile.nickname or "",
            "receiver_phone": profile.phone or "",
            "receiver_address": profile.address or "",
        }

    @staticmethod
    def update_shipping_info(user_id: int, data: dict):
        user = UserRepository.get_user_with_profile(user_id)
        if not user:
            raise ValueError("用户不存在")

        profile = UserRepository.get_or_create_user_profile(user)

        profile.nickname = data["receiver_name"].strip()
        profile.phone = data["receiver_phone"].strip()
        profile.address = data["receiver_address"].strip()
        profile.save()

        return {
            "receiver_name": profile.nickname or "",
            "receiver_phone": profile.phone or "",
            "receiver_address": profile.address or "",
        }

    @staticmethod
    def get_profile_info(user_id: int):
        user = UserRepository.get_user_with_profile(user_id)
        if not user:
            raise ValueError("用户不存在")

        profile = UserRepository.get_or_create_user_profile(user)
        latest_application = UserRepository.get_latest_merchant_application(user)

        return {
            "username": user.username or "",
            "nickname": profile.nickname or "",
            "phone": profile.phone or "",
            "email": user.email or "",
            "avatar": profile.avatar or "",
            "role": profile.role or UserRoleChoices.CUSTOMER,
            "merchant_application_status": latest_application.status if latest_application else "",
            "merchant_application_shop_name": latest_application.shop_name if latest_application else "",
            "merchant_application_review_remark": latest_application.review_remark if latest_application else "",
        }

    @staticmethod
    def update_profile_info(user_id: int, data: dict):
        user = UserRepository.get_user_with_profile(user_id)
        if not user:
            raise ValueError("用户不存在")

        profile = UserRepository.get_or_create_user_profile(user)

        if "nickname" in data:
            profile.nickname = data["nickname"].strip()

        if "phone" in data:
            profile.phone = data["phone"].strip()

        if "avatar" in data:
            profile.avatar = data["avatar"].strip()

        if "email" in data:
            user.email = data["email"].strip()

        user.save()
        profile.save()

        latest_application = UserRepository.get_latest_merchant_application(user)

        return {
            "username": user.username or "",
            "nickname": profile.nickname or "",
            "phone": profile.phone or "",
            "email": user.email or "",
            "avatar": profile.avatar or "",
            "role": profile.role or UserRoleChoices.CUSTOMER,
            "merchant_application_status": latest_application.status if latest_application else "",
            "merchant_application_shop_name": latest_application.shop_name if latest_application else "",
            "merchant_application_review_remark": latest_application.review_remark if latest_application else "",
        }