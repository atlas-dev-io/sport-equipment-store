from django.urls import path

from dashboard.controllers.dashboard_controller import (
    AdminDashboardAnalyticsController,
    AdminDashboardStatsController,
)

urlpatterns = [
    path("admin/stats/", AdminDashboardStatsController.as_view(), name="admin-dashboard-stats"),
    path("admin/analytics/", AdminDashboardAnalyticsController.as_view(), name="admin-dashboard-analytics"),
]