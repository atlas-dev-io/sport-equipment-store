from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsMerchantOrAdminOrReadOnly(BasePermission):
    """
    商品权限：
    - 列表/详情：任何人可读
    - 新增：仅商家或管理员
    - 修改/删除：管理员可操作；商家只能操作自己的商品
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False

        profile = getattr(user, "profile", None)
        if not profile:
            return False

        return profile.role in ["merchant", "admin"]

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False

        profile = getattr(user, "profile", None)
        if not profile:
            return False

        if profile.role == "admin":
            return True

        if profile.role == "merchant" and obj.merchant_id == user.id:
            return True

        return False