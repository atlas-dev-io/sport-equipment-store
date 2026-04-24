from django.conf import settings
from django.db import models

from orders.models import Order


class PaymentMethodChoices(models.TextChoices):
    ALIPAY = "alipay", "支付宝"
    WECHAT = "wechat", "微信支付"
    MOCK = "mock", "模拟支付"


class PaymentStatusChoices(models.TextChoices):
    UNPAID = "unpaid", "未支付"
    SUCCESS = "success", "支付成功"
    FAILED = "failed", "支付失败"
    REFUNDED = "refunded", "已退款"


class Payment(models.Model):
    """
    支付记录表
    MVP 阶段先支持模拟支付
    """
    payment_no = models.CharField(max_length=64,unique=True,verbose_name="支付单号",db_comment="支付记录唯一编号",)
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name="payment",verbose_name="订单",db_comment="关联订单，一个订单对应一条主要支付记录",)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="payments",verbose_name="用户",db_comment="支付用户",)
    method = models.CharField(max_length=20,choices=PaymentMethodChoices.choices,default=PaymentMethodChoices.MOCK,verbose_name="支付方式",db_comment="支付方式：支付宝、微信、模拟支付",)
    status = models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.UNPAID,verbose_name="支付状态",db_comment="支付状态：未支付、成功、失败、退款",)
    amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="支付金额",db_comment="本次支付金额",)
    third_party_trade_no = models.CharField(max_length=100,blank=True,default="",verbose_name="第三方交易号",db_comment="第三方支付平台返回的交易号，可为空",)
    paid_at = models.DateTimeField(null=True,blank=True,verbose_name="支付时间",db_comment="支付成功时间，可为空",)
    remark = models.CharField(max_length=255,blank=True,default="",verbose_name="备注",db_comment="支付备注说明",)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="创建时间",db_comment="记录创建时间",)
    updated_at = models.DateTimeField(auto_now=True,verbose_name="更新时间",db_comment="记录最后更新时间",)

    class Meta:
        db_table = "payment"
        db_table_comment = "支付记录表"
        verbose_name = "支付记录"
        verbose_name_plural = "支付记录"
        ordering = ["-id"]

    def __str__(self):
        return self.payment_no