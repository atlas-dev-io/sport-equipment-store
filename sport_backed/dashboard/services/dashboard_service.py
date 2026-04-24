from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from dashboard.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    STATUS_LABEL_MAP = {
        "pending_payment": "待支付",
        "paid": "已支付",
        "shipped": "已发货",
        "completed": "已完成",
        "canceled": "已取消",
        "refunded": "已退款",
    }

    @staticmethod
    def _check_admin_dashboard_permission(user):
        role = DashboardRepository.get_user_role(user)
        if role not in ["merchant", "admin"]:
            raise ValueError("当前账号无权访问管理端统计")
        return role

    @staticmethod
    def _format_decimal(value):
        if value is None:
            return Decimal("0.00")
        return Decimal(value).quantize(Decimal("0.00"))

    @staticmethod
    def _get_sales_amount(order_queryset, order_item_queryset, role):
        if role == "admin":
            return order_queryset.filter(
                status__in=DashboardRepository.SALE_STATUS_LIST
            ).aggregate(total=Sum("pay_amount"))["total"] or Decimal("0.00")

        return order_item_queryset.filter(
            order__status__in=DashboardRepository.SALE_STATUS_LIST
        ).aggregate(total=Sum("subtotal_amount"))["total"] or Decimal("0.00")

    @staticmethod
    def _get_today_sales_amount(order_queryset, order_item_queryset, role, target_date):
        if role == "admin":
            return order_queryset.filter(
                status__in=DashboardRepository.SALE_STATUS_LIST,
                created_at__date=target_date,
            ).aggregate(total=Sum("pay_amount"))["total"] or Decimal("0.00")

        return order_item_queryset.filter(
            order__status__in=DashboardRepository.SALE_STATUS_LIST,
            order__created_at__date=target_date,
        ).aggregate(total=Sum("subtotal_amount"))["total"] or Decimal("0.00")

    @staticmethod
    def _get_range_sales_amount(order_queryset, order_item_queryset, role, start_date, end_date):
        if role == "admin":
            return order_queryset.filter(
                status__in=DashboardRepository.SALE_STATUS_LIST,
                created_at__date__gte=start_date,
                created_at__date__lte=end_date,
            ).aggregate(total=Sum("pay_amount"))["total"] or Decimal("0.00")

        return order_item_queryset.filter(
            order__status__in=DashboardRepository.SALE_STATUS_LIST,
            order__created_at__date__gte=start_date,
            order__created_at__date__lte=end_date,
        ).aggregate(total=Sum("subtotal_amount"))["total"] or Decimal("0.00")

    @staticmethod
    def get_admin_dashboard_stats(user):
        analytics = DashboardService.get_admin_dashboard_analytics(user)
        return analytics["overview"]

    @staticmethod
    def get_admin_dashboard_analytics(user):
        role = DashboardService._check_admin_dashboard_permission(user)

        product_queryset = DashboardRepository.get_product_queryset(user, role)
        order_queryset = DashboardRepository.get_order_queryset(user, role)
        order_item_queryset = DashboardRepository.get_order_item_queryset(user, role)

        today = timezone.localdate()
        seven_day_start = today - timedelta(days=6)

        product_count = product_queryset.count()
        order_count = order_queryset.count()
        pending_order_count = order_queryset.filter(status="paid").count()

        today_sales_amount = DashboardService._get_today_sales_amount(
            order_queryset, order_item_queryset, role, today
        )
        seven_day_sales_amount = DashboardService._get_range_sales_amount(
            order_queryset, order_item_queryset, role, seven_day_start, today
        )
        total_sales_amount = DashboardService._get_sales_amount(
            order_queryset, order_item_queryset, role
        )

        overview = {
            "product_count": product_count,
            "order_count": order_count,
            "pending_order_count": pending_order_count,
            "today_sales_amount": DashboardService._format_decimal(today_sales_amount),
            "seven_day_sales_amount": DashboardService._format_decimal(seven_day_sales_amount),
            "total_sales_amount": DashboardService._format_decimal(total_sales_amount),
            "role": role,
        }

        raw_status_distribution = DashboardRepository.get_status_distribution(order_queryset)
        order_status_distribution = [
            {
                "status": item["status"],
                "label": DashboardService.STATUS_LABEL_MAP.get(item["status"], item["status"]),
                "count": item["count"],
            }
            for item in raw_status_distribution
        ]

        seven_day_order_trend = []
        for i in range(6, -1, -1):
            target_date = today - timedelta(days=i)

            day_order_count = order_queryset.filter(created_at__date=target_date).count()
            day_sales_amount = DashboardService._get_today_sales_amount(
                order_queryset, order_item_queryset, role, target_date
            )

            seven_day_order_trend.append(
                {
                    "date": target_date.strftime("%m-%d"),
                    "order_count": day_order_count,
                    "sales_amount": DashboardService._format_decimal(day_sales_amount),
                }
            )

        raw_category_ranking = DashboardRepository.get_category_sales_ranking(order_item_queryset, limit=8)
        category_sales_ranking = [
            {
                "category_name": item["product__category__name"] or "未分类",
                "sales_quantity": item["sales_quantity"] or 0,
                "sales_amount": DashboardService._format_decimal(item["sales_amount"]),
            }
            for item in raw_category_ranking
        ]

        sales_statistics = [
            {
                "label": "今日销售额",
                "value": DashboardService._format_decimal(today_sales_amount),
            },
            {
                "label": "近7天销售额",
                "value": DashboardService._format_decimal(seven_day_sales_amount),
            },
            {
                "label": "累计销售额",
                "value": DashboardService._format_decimal(total_sales_amount),
            },
            {
                "label": "待发货订单",
                "value": DashboardService._format_decimal(Decimal(str(pending_order_count))),
            },
        ]

        return {
            "overview": overview,
            "order_status_distribution": order_status_distribution,
            "seven_day_order_trend": seven_day_order_trend,
            "category_sales_ranking": category_sales_ranking,
            "sales_statistics": sales_statistics,
        }