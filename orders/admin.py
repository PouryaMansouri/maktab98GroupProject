from django.contrib import admin
from .models import Order, OrderItem, Table

# Register your models here.


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "create_time", "paid")
    list_filter = ("paid",)
    inlines = (OrderItemInline,)
