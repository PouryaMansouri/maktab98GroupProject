from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Q

from .utils_dashboard import (
    MostSellerProducts,
    OrdersManager,
    BestCustomer,
    MostSellerCategories,
    ComparisonCustomers,
    ComparisonOrders,
)
from utils import send_otp_code
from accounts.models import Customer, Personnel
from cafe.models import Product
from orders.models import Order, OrderItem
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
            request.session["my_datetime"] = current_datetime.isoformat()
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
                messages.error(request, "The code or phone_number is wrong!", "error")
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
        orders_with_costs = orders.orders_with_costs(10)
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

        best_customers = BestCustomer()
        best_customers_all = best_customers.best_customers_all(5)
        best_customers_year = best_customers.best_customers_year(5)
        best_customers_month = best_customers.best_customers_month(5)
        best_customers_week = best_customers.best_customers_week(5)
        customers_count = best_customers.count_customers()
        best_customers_list = [
            best_customers_all,
            best_customers_year,
            best_customers_month,
            best_customers_week,
        ]
        best_customer_titles = [
            "Best customers of all time",
            "Best customers of all year",
            "Best customers of all month",
            "Best customers of all week",
        ]

        best_customers_with_title = zip(best_customers_list, best_customer_titles)

        general_data_list = [
            total_sales,
            orders_count,
            customers_count,
            personnels_count,
        ]
        general_data_titles = [
            "total sales",
            "orders count",
            "customers count",
            "personnels count",
        ]

        general_data_with_title = zip(general_data_list, general_data_titles)

        context = {
            "best_categories_all": best_categories_all,
            "best_categories_year": best_categories_year,
            "best_categories_month": best_categories_month,
            "best_categories_week": best_categories_week,
            "best_customers_with_title": best_customers_with_title,
            "customers_count": customers_count,
            "orders_count": orders_count,
            "total_sales": total_sales,
            "orders_with_costs": orders_with_costs,
            "each_hour": each_hour,
            "orders_count_by_status": orders_count_by_status,
            "general_data_with_title": general_data_with_title,
        }
        return render(request, "accounts/dashboard.html", context=context)


class SalesDashboardView(View):
    def get(self, request):
        most_seller = MostSellerProducts()
        most_seller_all = most_seller.most_seller_products_all(3)
        most_seller_year = most_seller.most_seller_products_year(3)
        most_seller_month = most_seller.most_seller_products_month(3)
        most_seller_week = most_seller.most_seller_products_week(3)

        most_seller_morning = most_seller.most_seller_products_morning(3)
        most_seller_noon = most_seller.most_seller_products_noon(3)
        most_seller_night = most_seller.most_seller_products_night(3)

        compare_orders = ComparisonOrders()
        compare_orders_annual = compare_orders.compare_order_annual()
        compare_orders_monthly = compare_orders.compare_order_monthly()
        compare_orders_weekly = compare_orders.compare_order_weekly()
        compare_orders_daily = compare_orders.compare_order_daily()

        compare_orders_list = [
            compare_orders_annual,
            compare_orders_monthly,
            compare_orders_weekly,
            compare_orders_daily,
        ]

        most_seller_products_list = [
            most_seller_all,
            most_seller_year,
            most_seller_month,
            most_seller_week,
        ]
        

        compare_orders_title = [
            "Annual Sales",
            "Monthly Sales",
            "Weekly Sales",
            "Daily Sales",
        ]
        most_seller_products_title = [
            "Top Selling Products of all time",
            "Top Selling Products of the year",
            "Top Selling Products of the month",
            "Top Selling Products of the week",
        ]


        compare_orders_with_titles = zip(compare_orders_list, compare_orders_title)
        most_seller_products_with_titles = zip(
            most_seller_products_list, most_seller_products_title
        )

        context = {
            "compare_orders_with_titles": compare_orders_with_titles,
            "most_seller_products_with_titles": most_seller_products_with_titles,
            "most_seller_morning": most_seller_morning,
            "most_seller_noon": most_seller_noon,
            "most_seller_night": most_seller_night,
        }
        return render(request, "accounts/sales_dashboard.html", context=context)


class OrderDetailView(View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        total_price = order.get_total_price()
        return render(request, "accounts/order_detail.html", {"order": order, "total_price": total_price})

class ShowAllOrders(TemplateView):
    template_name = "accounts/all_orders_table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders_manager = OrdersManager()
        orders_with_costs = orders_manager.orders_with_costs(None)
        context["orders_with_costs"] = orders_with_costs
        return context
