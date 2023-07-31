from django.contrib import admin
from .models import Category,Product ,Customer

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CategoryAdmin(admin.ModelAdmin):
    pass
