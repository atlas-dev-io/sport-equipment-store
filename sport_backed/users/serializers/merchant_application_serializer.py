from rest_framework import serializers

from users.models import MerchantApplication


class MerchantApplicationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    reviewed_by_username = serializers.CharField(source="reviewed_by.username", read_only=True, default="")

    class Meta:
        model = MerchantApplication
        fields = [
            "id",
            "user",
            "username",
            "shop_name",
            "contact_name",
            "contact_phone",
            "application_reason",
            "status",
            "review_remark",
            "reviewed_by",
            "reviewed_by_username",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]


class MerchantApplicationReviewSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["approved", "rejected"])
    review_remark = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        default="",
    )