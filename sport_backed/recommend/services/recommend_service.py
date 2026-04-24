from collections import defaultdict
from decimal import Decimal

from django.utils import timezone

from recommend.repositories.recommend_repository import RecommendRepository


class RecommendService:
    """
    规则版推荐服务：
    1. 最近浏览分类优先
    2. 收藏品牌优先
    3. 收藏分类加分
    4. 热门商品兜底
    5. 推荐结果写入推荐日志
    """

    @staticmethod
    def record_browse_history(user, product_id: int):
        product = RecommendRepository.get_public_product_by_id(product_id)
        if not product:
            raise ValueError("商品不存在或不可浏览")

        history = RecommendRepository.get_browse_history_by_user_product(user, product)
        now = timezone.now()

        if history:
            history.viewed_at = now
            RecommendRepository.save_browse_history(history)
            return history

        return RecommendRepository.create_browse_history(
            user=user,
            product=product,
            viewed_at=now,
        )

    @staticmethod
    def list_browse_histories(user):
        return RecommendRepository.list_browse_histories(user)

    @staticmethod
    def toggle_favorite(user, product_id: int):
        product = RecommendRepository.get_public_product_by_id(product_id)
        if not product:
            raise ValueError("商品不存在或不可收藏")

        favorite = RecommendRepository.get_favorite_by_user_product(user, product)
        if favorite:
            RecommendRepository.delete_favorite(favorite)
            return {
                "product_id": product.id,
                "is_favorite": False,
            }

        RecommendRepository.create_favorite(user, product)
        return {
            "product_id": product.id,
            "is_favorite": True,
        }

    @staticmethod
    def get_favorite_status(user, product_id: int):
        return {
            "product_id": product_id,
            "is_favorite": RecommendRepository.exists_favorite(user, product_id),
        }

    @staticmethod
    def list_favorites(user):
        return RecommendRepository.list_favorites(user)

    @staticmethod
    def get_recommend_products(user, limit: int = 6):
        browse_histories = list(RecommendRepository.list_browse_histories(user)[:10])
        favorites = list(RecommendRepository.list_favorites(user)[:10])
        candidates = list(RecommendRepository.public_product_queryset()[:80])

        browse_category_score = defaultdict(int)
        favorite_brand_score = defaultdict(int)
        favorite_category_score = defaultdict(int)

        for idx, item in enumerate(browse_histories):
            category_id = item.product.category_id
            browse_category_score[category_id] += max(10, 40 - idx * 4)

        for idx, item in enumerate(favorites):
            if item.product.brand:
                favorite_brand_score[item.product.brand.strip()] += max(8, 35 - idx * 3)

            favorite_category_score[item.product.category_id] += max(6, 22 - idx * 2)

        scored_items = []
        for product in candidates:
            score = 0
            reasons = []

            if product.category_id in browse_category_score:
                current_score = browse_category_score[product.category_id]
                score += current_score
                reasons.append("近期浏览同类商品")

            product_brand = (product.brand or "").strip()
            if product_brand and product_brand in favorite_brand_score:
                current_score = favorite_brand_score[product_brand]
                score += current_score
                reasons.append("收藏品牌优先")

            if product.category_id in favorite_category_score:
                current_score = favorite_category_score[product.category_id]
                score += current_score
                reasons.append("收藏分类偏好")

            if product.is_recommend:
                score += 12
                reasons.append("平台推荐位商品")

            if product.sales_count > 0:
                hot_score = min(product.sales_count, 18)
                score += hot_score
                reasons.append("销量较高")

            if score <= 0:
                continue

            scored_items.append(
                {
                    "product": product,
                    "score": int(score),
                    "source": "rule_mvp",
                    "reason": "、".join(dict.fromkeys(reasons)),
                }
            )

        scored_items.sort(
            key=lambda x: (
                -x["score"],
                -x["product"].sales_count,
                -x["product"].id,
            )
        )

        result = scored_items[:limit]
        selected_ids = {item["product"].id for item in result}

        if len(result) < limit:
            fallback_products = [
                product for product in candidates if product.id not in selected_ids
            ]
            fallback_products.sort(
                key=lambda p: (
                    0 if p.is_recommend else 1,
                    -p.sales_count,
                    -p.id,
                )
            )

            for product in fallback_products:
                result.append(
                    {
                        "product": product,
                        "score": 10 if product.is_recommend else 6,
                        "source": "hot_fallback",
                        "reason": "热门商品兜底",
                    }
                )
                if len(result) >= limit:
                    break

        for item in result:
            RecommendRepository.create_recommend_log(
                user=user,
                product=item["product"],
                source=item["source"],
                score=Decimal(str(item["score"])),
                remark=item["reason"],
            )

        return result