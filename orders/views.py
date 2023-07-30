from django.shortcuts import render, get_object_or_404, redirect 
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm


class CartView(View):
    def get(self, request):
        return render(request, 'orders/cart.html')

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['total_price'] = int(item['price'])*  item['quantity']
        yield item 


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404 (Product, id=product_id)
        form = CartAddForm (request.POST) 
        if form.is_valid():
            cart.add(product,form.cleaned_data['quantity'])
        return redirect('orders: cart')

