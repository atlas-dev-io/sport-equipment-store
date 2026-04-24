from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.serializers.dashboard_serializer import AdminDashboardAnalyticsSerializer
from dashboard.services.dashboard_service import DashboardService


class AdminDashboardStatsController(APIView):
    """
    后台首页统计
    GET /api/dashboard/admin/stats/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = DashboardService.get_admin_dashboard_stats(request.user)
            return Response(
                {
                    "code": 200,
                    "message": "获取后台首页统计成功",
                    "data": data,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {
                    "code": 403,
                    "message": str(e),
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )


class AdminDashboardAnalyticsController(APIView):
    """
    后台首页可视化数据
    GET /api/dashboard/admin/analytics/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            result = DashboardService.get_admin_dashboard_analytics(request.user)
            data = AdminDashboardAnalyticsSerializer(result).data
            return Response(
                {
                    "code": 200,
                    "message": "获取后台可视化数据成功",
                    "data": data,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {
                    "code": 403,
                    "message": str(e),
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )