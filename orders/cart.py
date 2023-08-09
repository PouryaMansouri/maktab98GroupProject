from django.shortcuts import redirect

from cafe.models import Product

import json


CART_COOKIE_KEY = "cart"


class Cart:
    def __init__(self, request) -> None:
        cart = request.COOKIES.get(CART_COOKIE_KEY)
        if not cart:
            self.cart = {}
        else:
            self.cart = json.loads(cart)

    def add(self, product, quantity):
        product_id = str(product.id)
        if not product_id in self.cart:
            self.cart[product_id] = {
                "product": product.name,
                "quantity": quantity,
            }
        else:
            self.cart[product_id]["quantity"] += quantity



