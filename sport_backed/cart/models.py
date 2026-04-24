from django.conf import settings
from django.db import models

from products.models import Product


class Cart(models.Model):
    """
    购物车主表
    一个用户一个购物车
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="cart",verbose_name="用户",db_comment="所属用户，一个用户对应一个购物车",)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="创建时间",db_comment="购物车创建时间",)
    updated_at = models.DateTimeField(auto_now=True,verbose_name="更新时间",db_comment="购物车最后更新时间",)

    class Meta:
        db_table = "cart"
        db_table_comment = "购物车主表"
        verbose_name = "购物车"
        verbose_name_plural = "购物车"

    def __str__(self):
        return f"{self.user.username} 的购物车"


class CartItem(models.Model):
    """
    购物车明细表
    """
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items",verbose_name="购物车",db_comment="所属购物车",)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="cart_items",verbose_name="商品",db_comment="加入购物车的商品",)
    quantity = models.PositiveIntegerField(default=1,verbose_name="购买数量",db_comment="商品购买数量，最少为1",)
    checked = models.BooleanField(default=True,verbose_name="是否选中",db_comment="是否选中用于结算",)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="创建时间",db_comment="记录创建时间",)
    updated_at = models.DateTimeField(auto_now=True,verbose_name="更新时间",db_comment="记录最后更新时间",)

    class Meta:
        db_table = "cart_item"
        db_table_comment = "购物车明细表"
        verbose_name = "购物车明细"
        verbose_name_plural = "购物车明细"
        constraints = [models.UniqueConstraint(fields=["cart", "product"], name="uniq_cart_product")]

    def __str__(self):
        return f"{self.cart.user.username} - {self.product.name} - {self.quantity}"