from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    商品分类表
    支持一级分类、二级分类
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="分类名称", db_comment="商品分类名称，唯一")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name="父分类",
        db_comment="父级分类，可为空，为空表示一级分类",
    )
    sort_order = models.IntegerField(default=0, verbose_name="排序值", db_comment="分类排序值，越小越靠前")
    is_active = models.BooleanField(default=True, verbose_name="是否启用", db_comment="分类是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", db_comment="记录创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", db_comment="记录最后更新时间")

    class Meta:
        db_table = "category"
        db_table_comment = "商品分类表"
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.name


class ProductStatusChoices(models.TextChoices):
    DRAFT = "draft", "草稿"
    ON_SALE = "on_sale", "上架"
    OFF_SALE = "off_sale", "下架"


class Product(models.Model):
    """
    商品主表
    """
    merchant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="merchant_products",
        verbose_name="商家",
        db_comment="商品所属商家，可为空；MVP 阶段允许为空",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="商品分类",
        db_comment="商品所属分类",
    )
    name = models.CharField(max_length=200, verbose_name="商品名称", db_comment="商品名称")
    subtitle = models.CharField(max_length=255, blank=True, default="", verbose_name="商品副标题", db_comment="商品副标题，可为空")
    brand = models.CharField(max_length=100, blank=True, default="", verbose_name="品牌", db_comment="商品品牌，可为空")
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU编码", db_comment="商品唯一 SKU 编码")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="销售价格", db_comment="商品销售价格")
    market_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="市场价格", db_comment="商品划线价/市场价")
    stock = models.PositiveIntegerField(default=0, verbose_name="库存数量", db_comment="当前可售库存数量")
    low_stock_warning = models.PositiveIntegerField(default=10, verbose_name="低库存预警值", db_comment="当库存小于等于该值时触发低库存提醒")
    sales_count = models.PositiveIntegerField(default=0, verbose_name="销量", db_comment="商品累计销量")
    description = models.TextField(blank=True, default="", verbose_name="商品描述", db_comment="商品详情描述")
    main_image = models.URLField(max_length=255, blank=True, default="", verbose_name="主图地址", db_comment="商品主图 URL，可为空")
    status = models.CharField(
        max_length=20,
        choices=ProductStatusChoices.choices,
        default=ProductStatusChoices.ON_SALE,
        verbose_name="商品状态",
        db_comment="商品状态：草稿、上架、下架",
    )
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐", db_comment="是否推荐到首页或推荐位")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", db_comment="记录创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", db_comment="记录最后更新时间")

    class Meta:
        db_table = "product"
        db_table_comment = "商品主表"
        verbose_name = "商品"
        verbose_name_plural = "商品"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    商品图片表
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="商品",
        db_comment="所属商品",
    )
    image_url = models.URLField(max_length=255, verbose_name="图片地址", db_comment="商品图片 URL")
    alt_text = models.CharField(max_length=100, blank=True, default="", verbose_name="图片说明", db_comment="图片说明文字，可为空")
    sort_order = models.IntegerField(default=0, verbose_name="排序值", db_comment="图片排序值，越小越靠前")
    is_main = models.BooleanField(default=False, verbose_name="是否主图", db_comment="是否为主图")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", db_comment="记录创建时间")

    class Meta:
        db_table = "product_image"
        db_table_comment = "商品图片表"
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.name} - 图片{self.id}"


class InventoryChangeTypeChoices(models.TextChoices):
    INCREASE = "increase", "入库"
    DECREASE = "decrease", "出库"
    LOCK = "lock", "锁定库存"
    UNLOCK = "unlock", "释放库存"


class InventoryLog(models.Model):
    """
    库存变动日志表
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory_logs",
        verbose_name="商品",
        db_comment="关联商品",
    )
    change_type = models.CharField(
        max_length=20,
        choices=InventoryChangeTypeChoices.choices,
        verbose_name="变动类型",
        db_comment="库存变动类型：入库、出库、锁定、释放",
    )
    change_quantity = models.IntegerField(verbose_name="变动数量", db_comment="本次库存变动数量，可正可负")
    before_stock = models.IntegerField(default=0, verbose_name="变动前库存", db_comment="库存变动前的数量")
    after_stock = models.IntegerField(default=0, verbose_name="变动后库存", db_comment="库存变动后的数量")
    remark = models.CharField(max_length=255, blank=True, default="", verbose_name="备注", db_comment="库存变动备注说明")
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inventory_operations",
        verbose_name="操作人",
        db_comment="执行库存操作的用户，可为空",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", db_comment="记录创建时间")

    class Meta:
        db_table = "inventory_log"
        db_table_comment = "库存变动日志表"
        verbose_name = "库存日志"
        verbose_name_plural = "库存日志"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.product.name} - {self.change_type} - {self.change_quantity}"