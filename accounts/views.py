from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Q

from .utils_dashboard import MostSellerProducts, OrdersManager, BestCustomer, MostSellerCategories
from utils import send_otp_code
from accounts.models import Customer
from cafe.models import Product
from orders.models import Order , OrderItem
from .forms import UserCustomerLoginForm, OTPForm


from random import randint
import datetime
import pytz


# Create your views here.
class UserLoginView(View):
    form_class = UserCustomerLoginForm
    template_name = "accounts/personnel_login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("cafe:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        session = request.session["personnel_verify"] = {}
        if form.is_valid():
            current_datetime = datetime.datetime.now(tz=pytz.timezone("Asia/Tehran"))
            request.session['my_datetime'] = current_datetime.isoformat()
            cd = form.cleaned_data
            phone_number = cd["phone_number"]
            code = randint(1000, 9999)
            print(code)
            session["phone_number"] = phone_number
            session["code"] = code
            session["created_at"] = current_datetime.isoformat()

            return redirect("accounts:verify_personnel")

        return render(request, self.template_name, {"form": form})


class UserVerifyView(View):
    form_class = OTPForm

    def setup(self, request, *args, **kwargs):
        self.session = request.session["personnel_verify"]
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {"form": form}
        return render(request, "accounts/personnel_verify.html", context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        phone_number = self.session["phone_number"]
        if form.is_valid():
            cd = form.cleaned_data
            digit1 = cd["digit1"]
            digit2 = cd["digit2"]
            digit3 = cd["digit3"]
            digit4 = cd["digit4"]
            entered_code = int(digit1 + digit2 + digit3 + digit4)
            print(entered_code)

            user = authenticate(
                request,
                phone_number=phone_number,
                entered_code=entered_code,
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully", "success")
                return redirect("accounts:manage_orders")
            else:
                messages.error(
                    request, "The code or phone_number is wrong!", "error"
                )
                return redirect("accounts:verify_personnel")


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("cafe:home")


class ManageOrders(View):
    def get(self, request):
        orders = Order.objects.all()
        total_price = []
        for order in orders:
            total_price.append(order.get_total_price())
        orders_with_costs = zip(orders, total_price)
        # context = {'orders': orders, "total_price": total_price}
        context = {"orders_with_costs": orders_with_costs}
        return render(request, "accounts/manage_orders.html", context=context)


class DashboardView(View):
    def get(self, request):
        orders = OrdersManager()
        orders_with_costs = orders.orders_with_costs()
        orders_count = orders.count_orders()
        total_sales = orders.total_sales()
        each_hour = orders.get_peak_business_hours(8, 24)
        orders_count_by_status = orders.get_count_by_status()
        personnels_count = Personnel.objects.all().count()

        categories = MostSellerCategories()
        best_categories_all = categories.most_seller_categories_all(5)
        best_categories_year = categories.most_seller_categories_year(5)
        best_categories_month = categories.most_seller_categories_month(5)
        best_categories_week = categories.most_seller_categories_week(5)

        context = {
            # "total_sales": total_sales,
            "orders_with_costs": orders_with_costs,
            # "products": products,
        }
        return render(request, "accounts/dashboard.html", context=context)



class SalesDashboardView(View):
    def get(self, request):
        most_sellar = MostSellerProducts()
        most_sellar_all = most_sellar.most_seller_products_all(3)
        most_sellar_year = most_sellar.most_seller_products_year(3)
        most_sellar_month = most_sellar.most_seller_products_month(3)
        most_sellar_week = most_sellar.most_seller_products_week(3)
        customer = BestCustomer()
        customers_count = customer.count_customers()
        orders = OrdersManager()
        orders_count = orders.count_orders()
        total_sales = orders.total_sales()
        categories = MostSellerCategories()
        test = categories.most_seller_categories_year(3)
        context = {
            "most_sellar_all": most_sellar_all,
            "most_sellar_year": most_sellar_year,
            "most_sellar_month": most_sellar_month,
            "most_sellar_week": most_sellar_week,
            "customers_count": customers_count,
            "orders_count": orders_count,
            "total_sales": total_sales,
            "test": test,

        }
        return render(request, "accounts/sales_dashboard.html", context=context)

class OrderDetailView(View):
    def get(self, request , pk):
        order = Order.objects.get(pk=pk)
        return render(request, "accounts/order_detail.html", {'order': order})
