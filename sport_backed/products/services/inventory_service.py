from django.db import transaction

from products.models import InventoryChangeTypeChoices
from products.repositories.inventory_repository import InventoryRepository


class InventoryService:
    """
    库存服务层
    """

    @staticmethod
    def _get_user_role(user):
        profile = getattr(user, "profile", None)
        return profile.role if profile else ""

    @staticmethod
    def _check_permission(user):
        role = InventoryService._get_user_role(user)
        if role not in ["merchant", "admin"]:
            raise ValueError("当前账号无权访问库存管理")
        return role

    @staticmethod
    def get_inventory_list(user, keyword="", low_stock_only=False, status=""):
        InventoryService._check_permission(user)

        queryset = InventoryRepository.product_queryset_by_role(user)
        queryset = InventoryRepository.filter_inventory_queryset(
            queryset=queryset,
            keyword=keyword,
            low_stock_only=low_stock_only,
            status=status,
        )
        return queryset

    @staticmethod
    def get_inventory_log_list(user, product_id=None, keyword=""):
        InventoryService._check_permission(user)

        queryset = InventoryRepository.inventory_log_queryset_by_role(user)
        queryset = InventoryRepository.filter_inventory_log_queryset(
            queryset=queryset,
            product_id=product_id,
            keyword=keyword,
        )
        return queryset

    @staticmethod
    @transaction.atomic
    def adjust_inventory(user, product_id: int, change_type: str, quantity: int, remark: str = ""):
        InventoryService._check_permission(user)

        product = InventoryRepository.get_product_for_update(user, product_id)
        if not product:
            raise ValueError("商品不存在或无权操作")

        before_stock = product.stock

        if change_type == InventoryChangeTypeChoices.INCREASE:
            after_stock = before_stock + quantity
            signed_quantity = quantity
            default_remark = "后台手动入库"
        elif change_type == InventoryChangeTypeChoices.DECREASE:
            if before_stock < quantity:
                raise ValueError("库存不足，无法出库")
            after_stock = before_stock - quantity
            signed_quantity = -quantity
            default_remark = "后台手动出库"
        else:
            raise ValueError("库存调整类型不合法")

        product.stock = after_stock
        InventoryRepository.save_product(product)

        InventoryRepository.create_inventory_log(
            product=product,
            change_type=change_type,
            change_quantity=signed_quantity,
            before_stock=before_stock,
            after_stock=after_stock,
            remark=remark or default_remark,
            operator=user,
        )

        return product

    @staticmethod
    @transaction.atomic
    def update_low_stock_warning(user, product_id: int, low_stock_warning: int):
        InventoryService._check_permission(user)

        product = InventoryRepository.get_product_for_update(user, product_id)
        if not product:
            raise ValueError("商品不存在或无权操作")

        product.low_stock_warning = low_stock_warning
        InventoryRepository.save_product(product)
        return product