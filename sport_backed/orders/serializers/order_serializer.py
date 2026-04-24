from rest_framework import serializers

from orders.models import Order, OrderItem


class CreateOrderSerializer(serializers.Serializer):
    receiver_name = serializers.CharField(max_length=50)
    receiver_phone = serializers.CharField(max_length=20)
    receiver_address = serializers.CharField(max_length=255)
    remark = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        default="",
    )

    def validate_receiver_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("收货人不能为空")
        return value

    def validate_receiver_phone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("收货手机号不能为空")
        return value

    def validate_receiver_address(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("收货地址不能为空")
        return value


class OrderItemSimpleSerializer(serializers.ModelSerializer):
    merchant_id = serializers.IntegerField(source="product.merchant.id", read_only=True, default=None)
    merchant_username = serializers.CharField(source="product.merchant.username", read_only=True, default="")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_image",
            "product_price",
            "quantity",
            "subtotal_amount",
            "created_at",
            "merchant_id",
            "merchant_username",
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSimpleSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_no",
            "user",
            "username",
            "status",
            "total_amount",
            "pay_amount",
            "receiver_name",
            "receiver_phone",
            "receiver_address",
            "remark",
            "shipping_company",
            "tracking_no",
            "shipping_remark",
            "paid_at",
            "shipped_at",
            "completed_at",
            "created_at",
            "updated_at",
            "items",
        ]