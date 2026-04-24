from rest_framework import serializers

from products.models import InventoryChangeTypeChoices, InventoryLog, Product


class InventoryProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    merchant_username = serializers.CharField(source="merchant.username", read_only=True, default="")
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "sku",
            "stock",
            "low_stock_warning",
            "is_low_stock",
            "status",
            "category_name",
            "merchant_username",
            "updated_at",
        ]

    def get_is_low_stock(self, obj):
        return obj.stock <= obj.low_stock_warning


class InventoryAdjustSerializer(serializers.Serializer):
    change_type = serializers.ChoiceField(
        choices=[
            InventoryChangeTypeChoices.INCREASE,
            InventoryChangeTypeChoices.DECREASE,
        ]
    )
    quantity = serializers.IntegerField(min_value=1)
    remark = serializers.CharField(required=False, allow_blank=True, default="", max_length=255)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("调整数量必须大于0")
        return value


class InventoryWarningUpdateSerializer(serializers.Serializer):
    low_stock_warning = serializers.IntegerField(min_value=0)

    def validate_low_stock_warning(self, value):
        if value < 0:
            raise serializers.ValidationError("低库存预警值不能小于0")
        return value


class InventoryLogListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_sku = serializers.CharField(source="product.sku", read_only=True)
    operator_name = serializers.CharField(source="operator.username", read_only=True, default="")
    change_type_label = serializers.CharField(source="get_change_type_display", read_only=True)

    class Meta:
        model = InventoryLog
        fields = [
            "id",
            "product",
            "product_name",
            "product_sku",
            "change_type",
            "change_type_label",
            "change_quantity",
            "before_stock",
            "after_stock",
            "remark",
            "operator",
            "operator_name",
            "created_at",
        ]