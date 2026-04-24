from django.db import transaction
from django.utils import timezone

from users.models import MerchantApplicationStatusChoices, UserRoleChoices
from users.repositories.user_repository import UserRepository


class MerchantApplicationService:
    @staticmethod
    def _get_user_role(user):
        profile = getattr(user, "profile", None)
        return profile.role if profile else ""

    @staticmethod
    def _check_admin_permission(user):
        role = MerchantApplicationService._get_user_role(user)
        if role != UserRoleChoices.ADMIN:
            raise ValueError("当前账号无权审核商家申请")

    @staticmethod
    @transaction.atomic
    def submit_application(user_id: int, data: dict):
        user = UserRepository.get_user_with_profile(user_id)
        if not user:
            raise ValueError("用户不存在")

        profile = UserRepository.get_or_create_user_profile(user)

        if profile.role == UserRoleChoices.ADMIN:
            raise ValueError("管理员账号无需申请成为商家")

        if profile.role == UserRoleChoices.MERCHANT:
            raise ValueError("当前账号已经是商家")

        pending_application = UserRepository.get_pending_merchant_application(user)
        if pending_application:
            raise ValueError("你已有待审核的商家申请，请勿重复提交")

        application = UserRepository.create_merchant_application(
            user=user,
            shop_name=data["shop_name"].strip(),
            contact_name=data["contact_name"].strip(),
            contact_phone=data["contact_phone"].strip(),
            application_reason=data.get("application_reason", "").strip(),
            status=MerchantApplicationStatusChoices.PENDING,
        )
        return application

    @staticmethod
    def get_application_list(request_user, keyword="", status=""):
        MerchantApplicationService._check_admin_permission(request_user)

        queryset = UserRepository.merchant_application_queryset()

        if keyword:
            keyword = keyword.strip()
            queryset = queryset.filter(
                user__username__icontains=keyword
            ) | queryset.filter(
                shop_name__icontains=keyword
            ) | queryset.filter(
                contact_name__icontains=keyword
            ) | queryset.filter(
                contact_phone__icontains=keyword
            )

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by("-id")

    @staticmethod
    @transaction.atomic
    def review_application(request_user, application_id: int, action: str, review_remark: str = ""):
        MerchantApplicationService._check_admin_permission(request_user)

        application = UserRepository.get_merchant_application_by_id(application_id)
        if not application:
            raise ValueError("商家申请不存在")

        if application.status != MerchantApplicationStatusChoices.PENDING:
            raise ValueError("该申请已处理，不能重复审核")

        profile = UserRepository.get_or_create_user_profile(application.user)

        if action == MerchantApplicationStatusChoices.APPROVED:
            application.status = MerchantApplicationStatusChoices.APPROVED
            application.review_remark = review_remark.strip()
            application.reviewed_by = request_user
            application.reviewed_at = timezone.now()

            profile.role = UserRoleChoices.MERCHANT
            profile.save()

            UserRepository.save_merchant_application(application)
            return application

        if action == MerchantApplicationStatusChoices.REJECTED:
            application.status = MerchantApplicationStatusChoices.REJECTED
            application.review_remark = review_remark.strip()
            application.reviewed_by = request_user
            application.reviewed_at = timezone.now()

            if profile.role != UserRoleChoices.ADMIN:
                profile.role = UserRoleChoices.CUSTOMER
                profile.save()

            UserRepository.save_merchant_application(application)
            return application

        raise ValueError("审核动作不合法")