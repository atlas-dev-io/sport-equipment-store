from django.conf import settings
from django.db import models

from products.models import Product

class BrowseHistory(models.Model):
    """
    浏览记录表
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="browse_histories",verbose_name="用户",db_comment="浏览商品的用户",)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="browse_histories",verbose_name="商品",db_comment="被浏览的商品",)
    viewed_at = models.DateTimeField(auto_now_add=True,verbose_name="浏览时间",db_comment="用户浏览该商品的时间",)

    class Meta:
        db_table = "browse_history"
        db_table_comment = "商品浏览记录表"
        verbose_name = "浏览记录"
        verbose_name_plural = "浏览记录"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user.username} 浏览了 {self.product.name}"


class Favorite(models.Model):
    """
    商品收藏表
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="favorites",verbose_name="用户",db_comment="收藏商品的用户",)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="favorites",verbose_name="商品",db_comment="被收藏的商品",)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="收藏时间",db_comment="用户收藏该商品的时间",)

    class Meta:
        db_table = "favorite"
        db_table_comment = "商品收藏表"
        verbose_name = "商品收藏"
        verbose_name_plural = "商品收藏"
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="uniq_user_favorite_product")
        ]

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.product.name}"


class RecommendationLog(models.Model):
    """
    推荐日志表
    MVP 阶段先记录“给谁推荐了什么、为什么推荐”
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="recommendation_logs",verbose_name="用户",db_comment="被推荐商品的用户",)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="recommendation_logs",verbose_name="商品",db_comment="被推荐的商品",)
    source = models.CharField(max_length=50,default="manual",verbose_name="推荐来源",db_comment="推荐来源，如热门推荐、同类推荐、浏览推荐等",)
    score = models.DecimalField(max_digits=8,decimal_places=2,default=0,verbose_name="推荐分值",db_comment="推荐分值，MVP 阶段可简单记录",)
    remark = models.CharField(max_length=255,blank=True,default="",verbose_name="推荐说明",db_comment="推荐原因说明",)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="创建时间",db_comment="推荐记录创建时间",)

    class Meta:
        db_table = "recommendation_log"
        db_table_comment = "推荐日志表"
        verbose_name = "推荐日志"
        verbose_name_plural = "推荐日志"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user.username} <- {self.product.name}"