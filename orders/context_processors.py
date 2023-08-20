import json
import urllib

def dict_cookie(request):
    CART_COOKIE_KEY = "cart"
    if request.COOKIES.get(CART_COOKIE_KEY):
        cart_js = request.COOKIES.get(CART_COOKIE_KEY)
        decoded_cart_js = urllib.parse.unquote(cart_js)
        cart = json.loads(decoded_cart_js)
        length = len(cart.keys()) - 1
        total_price = cart.get("total_price") or 0
    else:
        cart = None
        total_price = 0
        length = 0 


    return {'cart': cart, "total_price": total_price, "length": length}
