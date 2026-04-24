from rest_framework import serializers

from orders.models import Order


class MockPayOrderSerializer(serializers.Serializer):
    """
    模拟支付请求参数
    """
    method = serializers.CharField(
        required=False,
        default="mock",
        help_text="支付方式，当前阶段默认 mock"
    )

    def validate_method(self, value):
        value = value.strip().lower()
        if value not in ["mock", "alipay", "wechat"]:
            raise serializers.ValidationError("支付方式不合法")
        return value


class OrderStatusActionSerializer(serializers.Serializer):
    """
    通用状态流转接口参数
    """
    remark = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        max_length=255,
        help_text="备注，可为空"
    )


class ShipOrderSerializer(serializers.Serializer):
    """
    发货参数
    """
    shipping_company = serializers.CharField(max_length=100)
    tracking_no = serializers.CharField(max_length=100)
    shipping_remark = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        max_length=255,
    )

    def validate_shipping_company(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("物流公司不能为空")
        return value

    def validate_tracking_no(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("快递单号不能为空")
        return value


class OrderStatusResultSerializer(serializers.ModelSerializer):
    """
    状态流转返回
    """

    class Meta:
        model = Order
        fields = [
            "id",
            "order_no",
            "user",
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
        ]