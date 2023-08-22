# django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# inner modules imports
from cafe.models import Product
from .forms import CustomerForm
from .models import Order, OrderItem, Table
from accounts.models import Customer
from dynamic.models import PageData

# third party imports
import json
import urllib.parse

# CART_COOKIE_KEY = "cart"


class CartView(View):
    def get(self, request):
        page_data = PageData.get_page_date("Cart_Page")
        context = {"page_data": page_data}
        return render(request, "orders/cart.html", context)


class CheckoutView(View):
    def get(self, request):
        try:
            last_phone_number = list(request.session.get("orders_info").values())[-1][
                -1
            ]
        except:
            last_phone_number = None
        initial_values = {"phone_number": last_phone_number}
        form = CustomerForm(initial=initial_values)
        page_data = PageData.get_page_date("Checkout_Page")
        context = {"form": form, "page_data": page_data}
        return render(request, "orders/checkout.html", context=context)


class AddOrderView(View):
    def setup(self, request, *args, **kwargs):
        self.CART_COOKIE_KEY = "cart"
        return super().setup(request, *args, **kwargs)

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
            cart_js = request.COOKIES.get(self.CART_COOKIE_KEY)
            decoded_cart_js = urllib.parse.unquote(cart_js)
            cart = json.loads(decoded_cart_js)
            for key, value in cart.items():
                if key != "total_price":
                    product = Product.objects.get(id=key)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=float(value["price"]),
                        quantity=value["quantity"],
                    )
                    session_order.append(
                        {
                            "product": value["name"],
                            "price": value["price"],
                            "quantity": value["quantity"],
                            "sub_total": value["sub_total"],
                        }
                    )
                    request.session.modified = True
                else:
                    total_cost = value
            session_order.append(total_cost)
            session_order.append(phone_number)
            response = redirect("orders:orders_history")
            response.delete_cookie(self.CART_COOKIE_KEY)
            return response


class OrderAccept(View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = "a"
        order.personnel = request.user
        order.save()
        return redirect("accounts:dashboard")


class OrderReject(View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = "r"
        order.personnel = request.user
        order.save()
        return redirect("accounts:dashboard")


class OrdersHistoryView(View):
    def get(self, request):
        session = request.session.get("orders_info")
        print(request.session)
        print(session)
        try:
            order_ids = list(session.keys())
            orders = Order.objects.filter(id__in=order_ids)
        except:
            orders = None
        page_data = PageData.get_page_date("Details_Page")
        return render(
            request,
            "orders/orders_history.html",
            {"orders": orders, "page_data": page_data},
        )


class ReorderView(View):
    form_class = CustomerForm

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        last_phone_number = list(request.session.get("orders_info").values())[-1][-1]
        initial_values = {"phone_number": last_phone_number}
        form = self.form_class(initial=initial_values)
        page_data = PageData.get_page_date("Checkout_Page")
        context = {"form": form, "page_data": page_data, "order": order}
        return render(request, "orders/reorder.html", context=context)

    def post(self, request, order_id):
        form = self.form_class(request.POST)
        order = Order.objects.get(id=order_id)
        if form.is_valid():
            cd = form.cleaned_data
            phone_number = cd["phone_number"]
            table_number = cd["table_number"]
            try:
                customer = Customer.objects.get(phone_number=phone_number)
            except:
                customer = Customer.objects.create(phone_number=phone_number)

            table = Table.objects.get(table_number=table_number)
            new_order = Order.objects.create(table=table, customer=customer)

            if request.session.get("orders_info"):
                session = request.session.get("orders_info")
            else:
                session = request.session["orders_info"] = {}

            session_order = session[str(new_order.id)] = []

            for orderitem in order.orderitem_set.all():
                OrderItem.objects.create(
                    order=new_order,
                    product=orderitem.product,
                    quantity=orderitem.quantity,
                    price=orderitem.price,
                )

                session_order.append(
                    {
                        "product": orderitem.product.name,
                        "price": float(orderitem.price),
                        "quantity": orderitem.quantity,
                        "sub_total": float(orderitem.get_cost()),
                    }
                )
                request.session.modified = True

            total_cost = float(order.get_total_price())
            session_order.append(total_cost)
            session_order.append(phone_number)
            return redirect("orders:orders_history")
