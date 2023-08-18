# django imports
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import admin
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# inner modules imports
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class csvImportForm(forms.Form):
    csv_upload = forms.FileField()


@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_available", "category")
    list_filter = ("is_available", "category")
    search_fields = ("name", "price")
    list_editable = ("is_available", "price")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                category_name = fields[5]
                try:
                    category = Category.objects.get(name=category_name)
                except ObjectDoesNotExist:
                    # Handle the case where the category does not exist
                    # You can choose to create a new category or handle the error as per your requirement
                    pass

                created = Product.objects.update_or_create(
                    name=fields[0],
                    image=fields[1],
                    is_available=fields[2],
                    description=fields[3],
                    price=fields[4],
                    category=category,
                )

            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        form = csvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)
