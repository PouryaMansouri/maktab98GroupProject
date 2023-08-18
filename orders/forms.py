# django imports
from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=0,
        max_value=9,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=1,
    )


class CustomerForm(forms.Form):
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput)
    table_number = forms.IntegerField()
