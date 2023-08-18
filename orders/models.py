# django imports
from django.db import models

# inner modules imports
from cafe.models import Product
from accounts.models import Personnel, Customer


class Table(models.Model):
    table_name = models.CharField(max_length=255, null=True, blank=True)
    table_number = models.IntegerField(null=True)


class Order(models.Model):
    STATUS_FIELDS = [("p", "Pending"), ("a", "Accepted"), ("r", "Rejected")]
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_FIELDS, default="p")
    paid = models.BooleanField(default=False)

    # Foreign keys
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    personnel = models.ForeignKey(Personnel, null=True, on_delete=models.PROTECT)
    table = models.ForeignKey(Table, null=True, on_delete=models.PROTECT)

    def get_total_price(self):
        return sum(item.get_cost() for item in self.orderitem_set.all())

    def __str__(self) -> str:
        return f"{self.status} || {self.create_time}"


class OrderItem(models.Model):
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Foreign keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product} || {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity
