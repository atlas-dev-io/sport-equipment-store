from django.urls import path

from users.controllers.admin_user_controller import (
    AdminMerchantApplicationListController,
    AdminMerchantApplicationReviewController,
    AdminUserDetailController,
    AdminUserListController,
)
from users.controllers.auth_controller import (
    CurrentUserController,
    LoginController,
    LogoutController,
    RegisterController,
)
from users.controllers.profile_controller import (
    BecomeMerchantController,
    ProfileInfoController,
    ShippingInfoController,
)

urlpatterns = [
    path("auth/register/", RegisterController.as_view(), name="user-register"),
    path("auth/login/", LoginController.as_view(), name="user-login"),
    path("auth/me/", CurrentUserController.as_view(), name="user-current"),
    path("auth/logout/", LogoutController.as_view(), name="user-logout"),

    path("profile/shipping/", ShippingInfoController.as_view(), name="user-shipping"),
    path("profile/info/", ProfileInfoController.as_view(), name="user-profile-info"),
    path("profile/become-merchant/", BecomeMerchantController.as_view(), name="user-become-merchant"),

    path("admin/users/", AdminUserListController.as_view(), name="admin-user-list"),
    path("admin/users/<int:id>/", AdminUserDetailController.as_view(), name="admin-user-detail"),
    path("admin/merchant-applications/", AdminMerchantApplicationListController.as_view(), name="admin-merchant-application-list"),
    path("admin/merchant-applications/<int:id>/review/", AdminMerchantApplicationReviewController.as_view(), name="admin-merchant-application-review"),
]