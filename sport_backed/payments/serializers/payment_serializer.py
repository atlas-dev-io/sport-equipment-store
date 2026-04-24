from rest_framework import serializers

from payments.models import Payment


class MockPaymentCreateSerializer(serializers.Serializer):
    """
    模拟支付请求参数
    """
    order_id = serializers.IntegerField(help_text="订单ID")
    method = serializers.CharField(
        required=False,
        default="mock",
        help_text="支付方式，默认 mock"
    )
    remark = serializers.CharField(
        required=False,
        allow_blank=True,
        default="模拟支付成功",
        max_length=255,
        help_text="支付备注"
    )

    def validate_order_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("订单ID不合法")
        return value

    def validate_method(self, value):
        value = value.strip().lower()
        if value not in ["mock", "alipay", "wechat"]:
            raise serializers.ValidationError("支付方式不合法")
        return value


class PaymentDetailSerializer(serializers.ModelSerializer):
    """
    支付记录详情
    """

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_no",
            "order",
            "user",
            "method",
            "status",
            "amount",
            "third_party_trade_no",
            "paid_at",
            "remark",
            "created_at",
            "updated_at",
        ]