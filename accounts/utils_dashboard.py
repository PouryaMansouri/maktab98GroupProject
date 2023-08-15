from django.db.models import Sum, Count
from cafe.models import Product
from accounts.models import Customer
from orders.models import Order
import datetime
import json


class MostSellerProducts:
    def most_seller_products_all(self, number):
        filtered_products = Product.objects.all()
        return self.count_quantity(filtered_products, number)

    def most_seller_products_year(self, number):
        current_year = datetime.datetime.now().year
        filtered_products = Product.objects.filter(
            orderitem__order__create_time__year=current_year
        )
        return self.count_quantity(filtered_products, number)

    def most_seller_products_month(self, number):
        current_month = datetime.datetime.now().date()
        first_day_month = current_month.replace(day=1)
        filtered_products = Product.objects.filter(
            orderitem__order__create_time__date__gte=first_day_month
        )
        return self.count_quantity(filtered_products, number)

    def most_seller_products_week(self, number):
        current_date = datetime.datetime.now().date()
        start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
        filtered_products = Product.objects.filter(
            orderitem__order__create_time__date__gte=start_of_week
        )
        return self.count_quantity(filtered_products, number)

    def most_seller_products_today(self, number):
        current_date = datetime.datetime.now().date()
        filtered_products = Product.objects.filter(
            orderitem__order__create_time__date=current_date
        )
        return self.count_quantity(filtered_products, number)

    def count_quantity(self, filtered_products, number):
        products = filtered_products.annotate(
            total_quantity=Sum("orderitem__quantity")
        ).order_by("-total_quantity")[:number]
        products_dict = self.to_dict(products)
        return products_dict

    def to_dict(self, most_sellar):
        product_quantity = {}
        for product in most_sellar:
            product_quantity[product.name] = [
                product.id,
                product.image.url,
                product.name,
                product.total_quantity,
                float(product.price),
                float(product.price) * product.total_quantity,
            ]
        return product_quantity

    def to_json(self, products_dict):
        return json.dumps(products_dict)
