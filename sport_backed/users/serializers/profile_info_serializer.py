from rest_framework import serializers


class ProfileInfoSerializer(serializers.Serializer):
    """
    个人资料返回序列化器
    """
    username = serializers.CharField()
    nickname = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    email = serializers.CharField(allow_blank=True)
    avatar = serializers.CharField(allow_blank=True)
    role = serializers.CharField(allow_blank=True)
    merchant_application_status = serializers.CharField(allow_blank=True)
    merchant_application_shop_name = serializers.CharField(allow_blank=True)
    merchant_application_review_remark = serializers.CharField(allow_blank=True)


class UpdateProfileInfoSerializer(serializers.Serializer):
    """
    更新个人资料请求序列化器
    """
    nickname = serializers.CharField(max_length=50, allow_blank=True, required=False)
    phone = serializers.CharField(max_length=20, allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    avatar = serializers.CharField(max_length=255, allow_blank=True, required=False)

    def validate_phone(self, value):
        value = value.strip()
        if value and not value.isdigit():
            raise serializers.ValidationError("手机号格式不正确")
        return value


class MerchantApplicationCreateSerializer(serializers.Serializer):
    """
    提交商家申请
    """
    shop_name = serializers.CharField(max_length=100)
    contact_name = serializers.CharField(max_length=50)
    contact_phone = serializers.CharField(max_length=20)
    application_reason = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        default="",
    )

    def validate_shop_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("店铺名称不能为空")
        return value

    def validate_contact_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("联系人不能为空")
        return value

    def validate_contact_phone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("联系电话不能为空")
        if not value.isdigit():
            raise serializers.ValidationError("联系电话格式不正确")
        return value