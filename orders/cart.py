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


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

    def save(self, destination):
        serialized_cart = json.dumps(self.cart)
        response = redirect(destination)
        response.set_cookie(CART_COOKIE_KEY, serialized_cart)
        return response

