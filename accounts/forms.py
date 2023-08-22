# django imports
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

# inner modules imports
from .models import Personnel
from orders.models import OrderItem


class PersonnelCreationForm(UserCreationForm):
    class Meta:
        model = Personnel
        fields = ["full_name", "email", "phone_number", "image"]


class PersonnelChangeForm(UserChangeForm):
    class Meta:
        model = Personnel
        fields = ["full_name", "email", "phone_number", "image"]


class UserCustomerLoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Phone Number",
                "label": "Phone Number",
            }
        )
    )


class OTPForm(forms.Form):
    digit1 = forms.CharField(
        max_length=1, widget=forms.TextInput(attrs={"maxlength": "1"})
    )
    digit2 = forms.CharField(
        max_length=1, widget=forms.TextInput(attrs={"maxlength": "1"})
    )
    digit3 = forms.CharField(
        max_length=1, widget=forms.TextInput(attrs={"maxlength": "1"})
    )
    digit4 = forms.CharField(
        max_length=1, widget=forms.TextInput(attrs={"maxlength": "1"})
    )


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ["order","price"]
