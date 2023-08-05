from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from utils import send_otp_code
from .models import OTPCode
from .forms import UserCustomerLoginForm, OTPForm

from random import randint

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


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("cafe:home")
