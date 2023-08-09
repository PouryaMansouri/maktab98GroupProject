from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from cafe.models import Product
from .forms import CartAddForm, CustomerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Table
from accounts.models import Customer


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        context = {"cart": cart}
        return render(request, "orders/cart.html", context)


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data["quantity"])
            response = cart.save("orders:cart")
        return response
        # return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        response = cart.save("orders:cart")
        return response
    
class CheckoutView(View):
    def get(self, request):
        form = CustomerForm()
        context = {"form": form}
        return render(request, "orders/checkout.html", context=context)



        