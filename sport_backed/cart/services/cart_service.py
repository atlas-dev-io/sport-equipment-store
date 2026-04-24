from cart.repositories.cart_repository import CartRepository


class CartService:
    """
    购物车服务层
    """

    @staticmethod
    def add_to_cart(user, product_id: int, quantity: int):
        cart = CartRepository.get_or_create_cart(user)
        product = CartRepository.get_product_by_id(product_id)

        if not product:
            raise ValueError("商品不存在")

        if product.status != "on_sale":
            raise ValueError("商品未上架，不能加入购物车")

        if not product.category.is_active:
            raise ValueError("商品分类不可用，不能加入购物车")

        if product.stock <= 0:
            raise ValueError("商品库存不足")

        cart_item = CartRepository.get_cart_item(cart, product)

        if cart_item:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                raise ValueError("加入后数量超过库存")
            cart_item.quantity = new_quantity
            CartRepository.save_cart_item(cart_item)
            return cart_item, False

        if quantity > product.stock:
            raise ValueError("加入数量超过库存")

        cart_item = CartRepository.create_cart_item(
            cart=cart,
            product=product,
            quantity=quantity,
            checked=True,
        )
        return cart_item, True

    @staticmethod
    def get_cart_detail(user):
        return CartRepository.get_cart_with_items(user)

    @staticmethod
    def update_cart_item(user, item_id: int, data: dict):
        cart_item = CartRepository.get_cart_item_by_id(item_id)
        if not cart_item:
            raise ValueError("购物车项不存在")

        if cart_item.cart.user_id != user.id:
            raise PermissionError("无权操作别人的购物车项")

        if "quantity" in data:
            quantity = data["quantity"]
            if quantity > cart_item.product.stock:
                raise ValueError("修改后数量超过库存")
            cart_item.quantity = quantity

        if "checked" in data:
            cart_item.checked = data["checked"]

        CartRepository.save_cart_item(cart_item)
        return cart_item

    @staticmethod
    def delete_cart_item(user, item_id: int):
        cart_item = CartRepository.get_cart_item_by_id(item_id)
        if not cart_item:
            raise ValueError("购物车项不存在")

        if cart_item.cart.user_id != user.id:
            raise PermissionError("无权删除别人的购物车项")

        CartRepository.delete_cart_item(cart_item)
        return True

    @staticmethod
    def clear_cart(user):
        cart = CartRepository.get_or_create_cart(user)
        CartRepository.clear_cart(cart)
        return True