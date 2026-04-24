from django.conf import settings
from django.db import models

from products.models import Product


class OrderStatusChoices(models.TextChoices):
    PENDING_PAYMENT = "pending_payment", "待支付"
    PAID = "paid", "已支付"
    SHIPPED = "shipped", "已发货"
    COMPLETED = "completed", "已完成"
    CANCELED = "canceled", "已取消"
    REFUNDED = "refunded", "已退款"


class Order(models.Model):
    """
    订单主表
    """
    order_no = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="订单编号",
        db_comment="订单唯一编号",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="用户",
        db_comment="下单用户",
    )
    status = models.CharField(
        max_length=30,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING_PAYMENT,
        verbose_name="订单状态",
        db_comment="订单状态：待支付、已支付、已发货、已完成、已取消、已退款",
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="订单总金额",
        db_comment="订单总金额",
    )
    pay_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="实付金额",
        db_comment="用户实际支付金额",
    )
    receiver_name = models.CharField(
        max_length=50,
        verbose_name="收货人",
        db_comment="收货人姓名",
    )
    receiver_phone = models.CharField(
        max_length=20,
        verbose_name="收货手机号",
        db_comment="收货手机号",
    )
    receiver_address = models.CharField(
        max_length=255,
        verbose_name="收货地址",
        db_comment="收货详细地址",
    )
    remark = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="订单备注",
        db_comment="用户下单备注，可为空",
    )

    shipping_company = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="物流公司",
        db_comment="发货物流公司，可为空",
    )
    tracking_no = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="快递单号",
        db_comment="物流快递单号，可为空",
    )
    shipping_remark = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="物流备注",
        db_comment="物流备注说明，可为空",
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="支付时间",
        db_comment="订单支付时间，可为空",
    )
    shipped_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="发货时间",
        db_comment="订单发货时间，可为空",
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="完成时间",
        db_comment="订单完成时间，可为空",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
        db_comment="订单创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        db_comment="订单最后更新时间",
    )

    class Meta:
        db_table = "order_info"
        db_table_comment = "订单主表"
        verbose_name = "订单"
        verbose_name_plural = "订单"
        ordering = ["-id"]

    def __str__(self):
        return self.order_no


class OrderItem(models.Model):
    """
    订单明细表
    说明：
    下单后要保留商品快照，避免商品后续改名、改价影响历史订单
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="订单",
        db_comment="所属订单",
    )
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="order_items",
        verbose_name="商品",
        db_comment="关联原始商品，可为空，防止商品删除后历史订单丢失",
    )
    product_name = models.CharField(
        max_length=200,
        verbose_name="商品名称快照",
        db_comment="下单时的商品名称快照",
    )
    product_image = models.URLField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="商品图片快照",
        db_comment="下单时的商品主图快照",
    )
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="商品单价快照",
        db_comment="下单时的商品单价快照",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="购买数量",
        db_comment="购买数量",
    )
    subtotal_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="小计金额",
        db_comment="当前明细小计金额",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
        db_comment="记录创建时间",
    )

    class Meta:
        db_table = "order_item"
        db_table_comment = "订单明细表"
        verbose_name = "订单明细"
        verbose_name_plural = "订单明细"

    def __str__(self):
        return f"{self.order.order_no} - {self.product_name}"