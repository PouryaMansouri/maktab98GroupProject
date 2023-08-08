from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category,Product ,Customer

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =('name' ,)
    search_fields = ('name' , )

@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display =('name' , 'price' , 'is_available' , 'category')
    list_filter = ('is_available' ,'category')
    search_fields = ('name' , 'price')
    list_editable= ('is_available','price')

@admin.register(Customer)
class CategoryAdmin(admin.ModelAdmin):
    list_display =('name' , 'phone_number')
    search_fields = ('name' , )