from django.urls import path

from products.controllers.inventory_controller import (
    InventoryAdjustController,
    InventoryLogListController,
    InventoryProductListController,
    InventoryWarningUpdateController,
)
from products.controllers.product_controller import (
    CategoryListController,
    ProductListCreateController,
    ProductRetrieveUpdateDestroyController,
)

urlpatterns = [
    path("categories/", CategoryListController.as_view(), name="category-list"),
    path("inventory/", InventoryProductListController.as_view(), name="inventory-product-list"),
    path("inventory/logs/", InventoryLogListController.as_view(), name="inventory-log-list"),
    path("inventory/<int:id>/adjust/", InventoryAdjustController.as_view(), name="inventory-adjust"),
    path("inventory/<int:id>/warning/", InventoryWarningUpdateController.as_view(), name="inventory-warning-update"),
    path("", ProductListCreateController.as_view(), name="product-list-create"),
    path("<int:id>/", ProductRetrieveUpdateDestroyController.as_view(), name="product-detail-update-delete"),
]