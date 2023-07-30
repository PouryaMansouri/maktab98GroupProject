CART_SESSION_ID='cart'

class cart:
    def __init__(self, request):
        self.session = request.session
        cart=self.session.get(CART_SESSION_ID)
        if not cart :
            cart=self.session[CART_SESSION_ID]={}
        self.cart=cart

    def ass (self, product , quantity):
        product_id=str(product.id)
