from django.db import models
from cafe.models import Product
from accounts.models import Personnel, Customer
# Create your models here.
class Order(models.Model):
    table_name = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    total_price = models.FloatField()

    # Foreign keys
    customer = models.ForeignKey(Customer, on_delete= models.PROTECT)
    personnel= models.ForeignKey(Personnel, null=True, on_delete= models.PROTECT)

class OrderItem(models.Model):
    quantity = models.IntegerField()
    
    # Foreign keys
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
