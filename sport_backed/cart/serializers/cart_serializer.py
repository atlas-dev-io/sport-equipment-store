from rest_framework import serializers

from cart.models import Cart, CartItem
from products.models import Product


class AddCartItemSerializer(serializers.Serializer):
    """
    加入购物车请求参数
    """
    product_id = serializers.IntegerField(help_text="商品ID")
    quantity = serializers.IntegerField(min_value=1, default=1, help_text="加入数量，至少为1")

    def validate_product_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("商品ID不合法")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    """
    更新购物车项请求参数
    quantity 和 checked 至少传一个
    """
    quantity = serializers.IntegerField(min_value=1, required=False, help_text="购买数量")
    checked = serializers.BooleanField(required=False, help_text="是否勾选")

    def validate(self, attrs):
        if "quantity" not in attrs and "checked" not in attrs:
            raise serializers.ValidationError("quantity 和 checked 至少传一个")
        return attrs


class CartProductSimpleSerializer(serializers.ModelSerializer):
    """
    购物车中商品简要信息
    """
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "subtitle",
            "brand",
            "sku",
            "price",
            "market_price",
            "stock",
            "main_image",
            "status",
            "category",
            "category_name",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    """
    购物车项返回
    """
    product = CartProductSimpleSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "checked",
            "subtotal",
            "created_at",
            "updated_at",
        ]

    def get_subtotal(self, obj):
        return str(obj.product.price * obj.quantity)


class CartDetailSerializer(serializers.ModelSerializer):
    """
    购物车详情返回
    """
    items = CartItemSerializer(many=True, read_only=True)
    total_count = serializers.SerializerMethodField()
    checked_count = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    checked_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "items",
            "total_count",
            "checked_count",
            "total_amount",
            "checked_amount",
            "created_at",
            "updated_at",
        ]

    def get_total_count(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_checked_count(self, obj):
        return sum(item.quantity for item in obj.items.all() if item.checked)

    def get_total_amount(self, obj):
        total = sum(item.product.price * item.quantity for item in obj.items.all())
        return str(total)

    def get_checked_amount(self, obj):
        total = sum(item.product.price * item.quantity for item in obj.items.all() if item.checked)
        return str(total)