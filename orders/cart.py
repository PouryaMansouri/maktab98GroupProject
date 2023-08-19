# django imports
from django.shortcuts import redirect

# inner modules imports
from cafe.models import Product

# third party imports
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
        for key, value in self.cart.items():
            yield key, value

    def add(self, product, quantity):
        product_id = str(product.id)
        if not product_id in self.cart:
            self.cart[product_id] = {
                "product": product.name,
                "quantity": quantity,
                "price": float(product.price),
                "sub_total": float(quantity * product.price),
            }
        else:
            self.cart[product_id]["quantity"] += quantity
            self.cart[product_id]["sub_total"] += quantity * float(product.price)

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

    def total_price(self):
        return sum(
            item["quantity"] * float(item["price"]) for item in self.cart.values()
        )

    def save(self, destination):
        serialized_cart = json.dumps(self.cart)
        response = redirect(destination)
        response.set_cookie(CART_COOKIE_KEY, serialized_cart)
        return response

    def delete(self, destination):
        response = redirect(destination)
        response.delete_cookie(CART_COOKIE_KEY)
        return response
