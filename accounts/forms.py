from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Personnel


class PersonnelCreationForm(UserCreationForm):
    class Meta:
        model = Personnel
        fields = ["full_name", "email", "phone_number", "image"]


class PersonnelChangeForm(UserChangeForm):
    class Meta:
        model = Personnel
        fields = ["full_name", "email", "phone_number", "image"]


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone Number",
                "label": "Phone Number",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()