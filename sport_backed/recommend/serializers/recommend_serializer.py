from rest_framework import serializers

from products.serializers.product_serializer import ProductListSerializer
from recommend.models import BrowseHistory, Favorite


class ProductActionSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("商品ID不合法")
        return value


class RecommendQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(required=False, default=6, min_value=1, max_value=20)


class FavoriteStatusQuerySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("商品ID不合法")
        return value


class BrowseHistoryItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = BrowseHistory
        fields = ["id", "product", "viewed_at"]


class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "product", "created_at"]


class FavoriteStatusSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    is_favorite = serializers.BooleanField()


class RecommendProductItemSerializer(serializers.Serializer):
    product = ProductListSerializer()
    score = serializers.IntegerField()
    source = serializers.CharField()
    reason = serializers.CharField()