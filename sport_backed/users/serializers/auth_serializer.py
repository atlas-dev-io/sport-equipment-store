from rest_framework import serializers

from users.models import UserRoleChoices


class RegisterSerializer(serializers.Serializer):
    """
    注册请求参数序列化器
    """
    username = serializers.CharField(max_length=150, help_text="用户名")
    password = serializers.CharField(write_only=True, min_length=6, max_length=128, help_text="密码，最少6位")
    confirm_password = serializers.CharField(write_only=True, min_length=6, max_length=128, help_text="确认密码")
    email = serializers.EmailField(required=False, allow_blank=True, help_text="邮箱，可为空")
    nickname = serializers.CharField(required=False, allow_blank=True, max_length=50, help_text="昵称，可为空")
    phone = serializers.CharField(required=False, allow_blank=True, max_length=20, help_text="手机号，可为空")
    role = serializers.ChoiceField(
        choices=UserRoleChoices.choices,
        required=False,
        default=UserRoleChoices.CUSTOMER,
        help_text="角色，默认 customer",
    )

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("用户名不能为空")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "两次输入的密码不一致"})
        return attrs


class LoginSerializer(serializers.Serializer):
    """
    登录请求参数序列化器
    """
    username = serializers.CharField(max_length=150, help_text="用户名")
    password = serializers.CharField(write_only=True, max_length=128, help_text="密码")

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("用户名不能为空")
        return value


class UserProfileSerializer(serializers.Serializer):
    """
    当前登录用户返回序列化器
    """
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_blank=True)
    is_active = serializers.BooleanField()
    date_joined = serializers.DateTimeField()

    role = serializers.CharField(allow_blank=True)
    nickname = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    avatar = serializers.CharField(allow_blank=True)
    gender = serializers.CharField(allow_blank=True)
    birthday = serializers.DateField(allow_null=True)
    address = serializers.CharField(allow_blank=True)

    merchant_application_status = serializers.CharField(allow_blank=True)
    merchant_application_shop_name = serializers.CharField(allow_blank=True)
    merchant_application_review_remark = serializers.CharField(allow_blank=True)