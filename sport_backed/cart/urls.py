from django.urls import path

from cart.controllers.cart_controller import (
    AddCartItemController,
    CartClearController,
    CartDetailController,
    CartItemUpdateDeleteController,
)

urlpatterns = [
    path("", CartDetailController.as_view(), name="cart-detail"),
    path("items/", AddCartItemController.as_view(), name="cart-item-add"),
    path("items/<int:id>/", CartItemUpdateDeleteController.as_view(), name="cart-item-update-delete"),
    path("clear/", CartClearController.as_view(), name="cart-clear"),
]