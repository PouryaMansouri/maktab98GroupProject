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

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["price"] = str(product.price)
            cart[str(product.id)]["sub_total"] = str(
                cart[str(product.id)]["quantity"] * product.price
            )

        for key, value in cart.items():
            yield key, value

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

