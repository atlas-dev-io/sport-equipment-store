from django.contrib import admin

from products.models import Category, InventoryLog, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "sort_order", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "sku", "price", "stock", "status", "is_recommend", "category", "merchant")
    search_fields = ("name", "brand", "sku")
    list_filter = ("status", "is_recommend", "category")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "is_main", "sort_order", "created_at")
    search_fields = ("product__name",)


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "change_type", "change_quantity", "before_stock", "after_stock", "operator", "created_at")
    search_fields = ("product__name", "remark")
    list_filter = ("change_type",)