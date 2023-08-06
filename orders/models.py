from django.db import models
from cafe.models import Customer, Product
from accounts.models import Personnel
# Create your models here.
class Order(models.Model):
    STATUS_FIELDS = [('p', 'Pending'),('a','Aaccepted'),('r','Rejected')]
    table_name = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    total_price = models.FloatField()
    status = models.CharField(max_length=1, choices= STATUS_FIELDS, default= 'p')

    # Foreign keys
    customer = models.ForeignKey(Customer, on_delete= models.PROTECT)
    personnel= models.ForeignKey(Personnel, null=True, on_delete= models.PROTECT)

class OrderItem(models.Model):
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Foreign keys
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
