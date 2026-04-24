from django.db.models import QuerySet

from products.models import Product, ProductStatusChoices
from recommend.models import BrowseHistory, Favorite, RecommendationLog


class RecommendRepository:
    """
    推荐模块数据访问层
    """

    @staticmethod
    def public_product_queryset() -> QuerySet:
        return (
            Product.objects.select_related("category", "merchant")
            .prefetch_related("images")
            .filter(
                status=ProductStatusChoices.ON_SALE,
                category__is_active=True,
            )
            .order_by("-id")
        )

    @staticmethod
    def get_public_product_by_id(product_id: int):
        return RecommendRepository.public_product_queryset().filter(id=product_id).first()

    @staticmethod
    def get_browse_history_by_user_product(user, product):
        return BrowseHistory.objects.filter(user=user, product=product).first()

    @staticmethod
    def create_browse_history(user, product, viewed_at):
        return BrowseHistory.objects.create(
            user=user,
            product=product,
            viewed_at=viewed_at,
        )

    @staticmethod
    def save_browse_history(instance):
        instance.save()
        return instance

    @staticmethod
    def list_browse_histories(user):
        return (
            BrowseHistory.objects.select_related("product", "product__category", "product__merchant")
            .prefetch_related("product__images")
            .filter(
                user=user,
                product__status=ProductStatusChoices.ON_SALE,
                product__category__is_active=True,
            )
            .order_by("-viewed_at", "-id")
        )

    @staticmethod
    def get_favorite_by_user_product(user, product):
        return Favorite.objects.filter(user=user, product=product).first()

    @staticmethod
    def create_favorite(user, product):
        return Favorite.objects.create(user=user, product=product)

    @staticmethod
    def delete_favorite(instance):
        instance.delete()

    @staticmethod
    def list_favorites(user):
        return (
            Favorite.objects.select_related("product", "product__category", "product__merchant")
            .prefetch_related("product__images")
            .filter(
                user=user,
                product__status=ProductStatusChoices.ON_SALE,
                product__category__is_active=True,
            )
            .order_by("-created_at", "-id")
        )

    @staticmethod
    def exists_favorite(user, product_id: int) -> bool:
        return Favorite.objects.filter(user=user, product_id=product_id).exists()

    @staticmethod
    def create_recommend_log(user, product, source: str, score, remark: str = ""):
        return RecommendationLog.objects.create(
            user=user,
            product=product,
            source=source,
            score=score,
            remark=remark,
        )