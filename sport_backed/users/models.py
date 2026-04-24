from django.conf import settings
from django.db import models


class UserRoleChoices(models.TextChoices):
    CUSTOMER = "customer", "消费者"
    MERCHANT = "merchant", "商家"
    ADMIN = "admin", "管理员"


class UserProfile(models.Model):
    """
    用户扩展信息表
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="用户",
        db_comment="关联 Django 内置用户表 auth_user",
    )
    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.CUSTOMER,
        verbose_name="角色",
        db_comment="用户角色：消费者、商家、管理员",
    )
    nickname = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="昵称",
        db_comment="用户昵称，可为空",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="手机号",
        db_comment="用户手机号，可为空",
    )
    avatar = models.URLField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="头像地址",
        db_comment="用户头像 URL，可为空",
    )
    gender = models.CharField(
        max_length=10,
        blank=True,
        default="",
        verbose_name="性别",
        db_comment="用户性别，可为空",
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name="生日",
        db_comment="用户生日，可为空",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="默认地址",
        db_comment="用户默认收货地址，可为空",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
        db_comment="记录创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        db_comment="记录最后更新时间",
    )

    class Meta:
        db_table = "user_profile"
        db_table_comment = "用户扩展信息表"
        verbose_name = "用户扩展信息"
        verbose_name_plural = "用户扩展信息"

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class MerchantApplicationStatusChoices(models.TextChoices):
    PENDING = "pending", "待审核"
    APPROVED = "approved", "已通过"
    REJECTED = "rejected", "已拒绝"


class MerchantApplication(models.Model):
    """
    商家申请表
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="merchant_applications",
        verbose_name="申请用户",
        db_comment="提交商家申请的用户",
    )
    shop_name = models.CharField(
        max_length=100,
        verbose_name="店铺名称",
        db_comment="申请中的店铺名称",
    )
    contact_name = models.CharField(
        max_length=50,
        verbose_name="联系人",
        db_comment="联系人姓名",
    )
    contact_phone = models.CharField(
        max_length=20,
        verbose_name="联系电话",
        db_comment="联系人手机号",
    )
    application_reason = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="申请说明",
        db_comment="申请说明，可为空",
    )
    status = models.CharField(
        max_length=20,
        choices=MerchantApplicationStatusChoices.choices,
        default=MerchantApplicationStatusChoices.PENDING,
        verbose_name="审核状态",
        db_comment="审核状态：待审核、已通过、已拒绝",
    )
    review_remark = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="审核备注",
        db_comment="管理员审核备注，可为空",
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_merchant_applications",
        verbose_name="审核人",
        db_comment="执行审核的管理员，可为空",
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="审核时间",
        db_comment="审核时间，可为空",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="申请时间",
        db_comment="申请创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        db_comment="记录最后更新时间",
    )

    class Meta:
        db_table = "merchant_application"
        db_table_comment = "商家申请表"
        verbose_name = "商家申请"
        verbose_name_plural = "商家申请"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user.username} - {self.shop_name} - {self.status}"