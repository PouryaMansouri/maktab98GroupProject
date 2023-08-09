from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Personnel, OTPCode


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

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        print(phone_number)
        OTPCode.objects.filter(phone_number=phone_number).delete()
        print("done")
        return phone_number



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
