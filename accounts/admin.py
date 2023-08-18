# django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# inner modules imports
from .forms import PersonnelCreationForm, PersonnelChangeForm
from .models import Personnel, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("phone_number",)
    search_fields = ("phone_number",)


class PersonnelAdmin(UserAdmin):
    add_form = PersonnelCreationForm
    form = PersonnelChangeForm

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
    search_fields = (
        "email",
        "full_name",
        "phone_number",
    )
    ordering = ("full_name",)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(Personnel, PersonnelAdmin)
