from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from cafe.models import Product
from .forms import CartAddForm, CustomerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Table
from accounts.models import Customer
from dynamic.models import PageData


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        page_data = PageData.get_page_date('Cart_Page')
        context = {"cart": cart, 'page_data': page_data}
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
        page_data = PageData.get_page_date('Checkout_Page')
        context = {"form": form, 'page_data': page_data}
        return render(request, "orders/checkout.html", context=context)


class AddOrderView(View):
    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone_number = cd["phone_number"]
            table_number = cd["table_number"]
            try:
                customer = Customer.objects.get(phone_number=phone_number)
            except:
                customer = Customer.objects.create(phone_number=phone_number)

            table = Table.objects.get(table_number=table_number)
            order = Order.objects.create(table=table, customer=customer)
            if request.session.get("orders_info"):
                session = request.session.get("orders_info")
            else:
                session = request.session["orders_info"] = {}

            session_order = session[str(order.id)] = []
            cart = Cart(request)
            for key, value in cart:
                product = Product.objects.get(id=key)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=float(value["price"]),
                    quantity=value["quantity"],
                )
                session_order.append(
                    {
                        "product": value["product"],
                        "price": value["price"],
                        "quantity": value["quantity"],
                        "sub_total": value["sub_total"],
                    }
                )
                request.session.modified = True
            total_cost = cart.total_price()
            session_order.append(total_cost)
            response = cart.delete("orders:order_detail")
            return response


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                product=item["product"],
                price=float(item["price"]),
                quantity=item["quantity"],
            )
        return redirect(
            "orders:order_detail",
        )


class OrderAccept(View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = "a"
        order.save()
        return redirect("accounts:dashboard")


class OrderReject(View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = "r"
        order.save()
        return redirect("accounts:dashboard")


class OrderDetailView(View):
    def get(self, request):
        session = request.session.get("orders_info")
        page_data = PageData.get_page_date('Details_Page')
        return render(request, "orders/detail.html", {"session": session, 'page_data': page_data})
