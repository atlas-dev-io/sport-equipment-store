from rest_framework import serializers

from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()


class AdminUserListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="profile.nickname", read_only=True, default="")
    phone = serializers.CharField(source="profile.phone", read_only=True, default="")
    role = serializers.CharField(source="profile.role", read_only=True, default="customer")
    avatar = serializers.CharField(source="profile.avatar", read_only=True, default="")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "date_joined",
            "nickname",
            "phone",
            "role",
            "avatar",
        ]


class AdminUserUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=["customer", "merchant", "admin"],
        required=False,
    )
    is_active = serializers.BooleanField(required=False)
    nickname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate_phone(self, value):
        value = value.strip()
        if value and not value.isdigit():
            raise serializers.ValidationError("手机号格式不正确")
        return value