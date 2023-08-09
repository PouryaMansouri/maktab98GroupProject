from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from utils import send_otp_code
from .models import OTPCode 
from orders.models import Order
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
        session = request.session["personnel_info"] = {}
        print(session)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            phone_number = cd["phone_number"]
            print(phone_number)
            code = randint(1000, 9999)
            # send_otp_code(phone_number, code)
            print(code)
            OTPCode.objects.create(phone_number=phone_number, code=code)
            session["phone_number"] = phone_number
            return redirect("accounts:verify_personnel")

        return render(request, self.template_name, {"form": form})


class UserVerifyPersonnelView(View):
    form_class = OTPForm

    def setup(self, request, *args, **kwargs):
        self.session = request.session["personnel_info"]
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {"form": form}
        return render(request, "accounts/personnel_verify.html", context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        phone_number = self.session["phone_number"]
        print(phone_number)
        otp_instance = OTPCode.objects.get(phone_number=phone_number)
        if form.is_valid():
            cd = form.cleaned_data
            digit1 = cd["digit1"]
            digit2 = cd["digit2"]
            digit3 = cd["digit3"]
            digit4 = cd["digit4"]
            entered_code = int(digit1 + digit2 + digit3 + digit4)
            print(entered_code)

            expired_time = datetime.datetime.now(tz=pytz.timezone("Asia/Tehran")) - datetime.timedelta(minutes=1)
            if (
                entered_code == otp_instance.code
                and otp_instance.created > expired_time
            ):
                user = authenticate(
                    request,
                    phone_number=phone_number,
                )
                print(user)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in Successfully", "success")
                    return redirect("accounts:manage_orders")
                else:
                    messages.error(
                        request, "The code or phone_number is wrong!", "error"
                    )
                    return redirect("accounts:verify_personnel")
            else:
                messages.error(request, "The code or phone_number is wrong!", "error")
                return redirect("accounts:verify_personnel")


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("cafe:home")

class ManageOrders(View):
    def get(self , request):
        orders = Order.objects.all()
        return render(request, 'accounts/manage_orders.html', {'orders': orders})