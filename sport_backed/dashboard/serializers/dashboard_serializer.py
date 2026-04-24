from rest_framework import serializers


class DashboardOverviewSerializer(serializers.Serializer):
    product_count = serializers.IntegerField()
    order_count = serializers.IntegerField()
    pending_order_count = serializers.IntegerField()
    today_sales_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    seven_day_sales_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_sales_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    role = serializers.CharField()


class OrderStatusDistributionItemSerializer(serializers.Serializer):
    status = serializers.CharField()
    label = serializers.CharField()
    count = serializers.IntegerField()


class SevenDayTrendItemSerializer(serializers.Serializer):
    date = serializers.CharField()
    order_count = serializers.IntegerField()
    sales_amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class CategorySalesRankingItemSerializer(serializers.Serializer):
    category_name = serializers.CharField()
    sales_quantity = serializers.IntegerField()
    sales_amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class SalesStatisticsItemSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.DecimalField(max_digits=12, decimal_places=2)


class AdminDashboardAnalyticsSerializer(serializers.Serializer):
    overview = DashboardOverviewSerializer()
    order_status_distribution = OrderStatusDistributionItemSerializer(many=True)
    seven_day_order_trend = SevenDayTrendItemSerializer(many=True)
    category_sales_ranking = CategorySalesRankingItemSerializer(many=True)
    sales_statistics = SalesStatisticsItemSerializer(many=True)