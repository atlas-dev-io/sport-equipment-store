from rest_framework import serializers

from products.models import Category, Product, ProductImage, ProductStatusChoices


class CategorySimpleSerializer(serializers.ModelSerializer):
    """
    分类简要序列化器
    """

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "sort_order", "is_active"]


class ProductImageSerializer(serializers.ModelSerializer):
    """
    商品图片序列化器
    """

    class Meta:
        model = ProductImage
        fields = ["id", "image_url", "alt_text", "sort_order", "is_main", "created_at"]


class ProductListSerializer(serializers.ModelSerializer):
    """
    商品列表序列化器
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
            "low_stock_warning",
            "sales_count",
            "main_image",
            "status",
            "is_recommend",
            "category",
            "category_name",
            "created_at",
            "updated_at",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    商品详情序列化器
    """
    category = CategorySimpleSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    merchant_username = serializers.CharField(source="merchant.username", read_only=True, default="")

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
            "low_stock_warning",
            "sales_count",
            "description",
            "main_image",
            "status",
            "is_recommend",
            "merchant",
            "merchant_username",
            "category",
            "images",
            "created_at",
            "updated_at",
        ]


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    商品新增/修改序列化器
    """

    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "subtitle",
            "brand",
            "sku",
            "price",
            "market_price",
            "stock",
            "description",
            "main_image",
            "status",
            "is_recommend",
        ]

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("商品名称不能为空")
        return value

    def validate_sku(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("SKU不能为空")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("销售价格不能小于0")
        return value

    def validate_market_price(self, value):
        if value < 0:
            raise serializers.ValidationError("市场价格不能小于0")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("库存不能小于0")
        return value

    def validate_status(self, value):
        valid_values = [choice[0] for choice in ProductStatusChoices.choices]
        if value not in valid_values:
            raise serializers.ValidationError("商品状态不合法")
        return value

    def validate(self, attrs):
        price = attrs.get("price")
        market_price = attrs.get("market_price")

        if price is not None and market_price is not None and market_price != 0 and market_price < price:
            raise serializers.ValidationError({"market_price": "市场价格不能小于销售价格"})

        return attrs