from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import PersonnelcreationForm, PersonelChangeForm
from .models import Personnel


# Register your models here.
class PersonnelAdmin(UserAdmin):
    add_form = PersonnelcreationForm
    form = PersonelChangeForm

    list_display = ("full_name", "phone_number", "email", "is_admin")
    list_filter = ("is_admin", "is_active")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone_number",
                    "image",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_admin", "is_active", "last_login")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone_number",
                    "image",
                    "password1",
                    "password2",
                ),
            },
        ),
        ("Permissions", {"fields": ("is_admin", "is_active")}),
    )
    search_fields = ("email", "full_name", "phone_number")
    ordering = ("full_name",)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(Personnel, PersonnelAdmin)
