from cart.models import Cart, CartItem
from products.models import Product


class CartRepository:
    """
    购物车仓库层
    """

    @staticmethod
    def get_or_create_cart(user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def get_cart_with_items(user):
        cart, _ = Cart.objects.prefetch_related(
            "items__product__category"
        ).get_or_create(user=user)
        return cart

    @staticmethod
    def get_product_by_id(product_id: int):
        return Product.objects.select_related("category", "merchant").filter(id=product_id).first()

    @staticmethod
    def get_cart_item(cart, product):
        return CartItem.objects.filter(cart=cart, product=product).first()

    @staticmethod
    def create_cart_item(cart, product, quantity=1, checked=True):
        return CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity,
            checked=checked,
        )

    @staticmethod
    def save_cart_item(cart_item: CartItem):
        cart_item.save()
        return cart_item

    @staticmethod
    def get_cart_item_by_id(item_id: int):
        return CartItem.objects.select_related("cart", "product", "product__category").filter(id=item_id).first()

    @staticmethod
    def delete_cart_item(cart_item: CartItem):
        cart_item.delete()

    @staticmethod
    def clear_cart(cart):
        cart.items.all().delete()