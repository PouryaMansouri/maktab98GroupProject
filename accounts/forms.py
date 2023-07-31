from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Personnel


class PersonnelCreationForm(UserCreationForm):
    # password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    # password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = Personnel
        fields = ["full_name", "email", "phone_number", "image"]

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd["password1"] and cd["password2"] and cd["password1"] != cd["password2"]:
    #         raise ValidationError("Passwords must be match!")

    #     return cd["password2"]

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user


class PersonnelChangeForm(UserChangeForm):
    # password = ReadOnlyPasswordHashField(
    #     label="Password",
    #     help_text=(
    #         "you can change the password " 'using <a href="../password/">this form</a>.'
    #     ),
    # )

    class Meta:
        model = Personnel
        fields = ["full_name", "email", "phone_number", "image"]
