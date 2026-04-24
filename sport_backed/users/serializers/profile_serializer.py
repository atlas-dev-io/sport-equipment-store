from rest_framework import serializers


class ShippingInfoSerializer(serializers.Serializer):
    """
    收货信息返回序列化器
    """
    receiver_name = serializers.CharField(allow_blank=True)
    receiver_phone = serializers.CharField(allow_blank=True)
    receiver_address = serializers.CharField(allow_blank=True)


class UpdateShippingInfoSerializer(serializers.Serializer):
    """
    更新收货信息请求序列化器
    """
    receiver_name = serializers.CharField(max_length=50)
    receiver_phone = serializers.CharField(max_length=20)
    receiver_address = serializers.CharField(max_length=255)

    def validate_receiver_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("收货人不能为空")
        return value

    def validate_receiver_phone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("手机号不能为空")
        return value

    def validate_receiver_address(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("收货地址不能为空")
        return value