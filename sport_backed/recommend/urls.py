from django.urls import path

from recommend.controllers.recommend_controller import (
    BrowseHistoryListController,
    BrowseHistoryRecordController,
    FavoriteListController,
    FavoriteStatusController,
    FavoriteToggleController,
    RecommendProductListController,
)

urlpatterns = [
    path("history/", BrowseHistoryListController.as_view(), name="browse-history-list"),
    path("history/record/", BrowseHistoryRecordController.as_view(), name="browse-history-record"),
    path("favorites/", FavoriteListController.as_view(), name="favorite-list"),
    path("favorites/status/", FavoriteStatusController.as_view(), name="favorite-status"),
    path("favorites/toggle/", FavoriteToggleController.as_view(), name="favorite-toggle"),
    path("products/", RecommendProductListController.as_view(), name="recommend-product-list"),
]