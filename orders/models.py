from django.db import models
from cafe.models import Product
from accounts.models import Personnel, Customer
from cafe.models import Customer, Product
from accounts.models import Personnel

# Create your models here.
class Order(models.Model):
    table_name = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    total_price = models.FloatField()
    paid=models.BooleanField(default=False)

    # Foreign keys
    customer = models.ForeignKey(Customer, on_delete= models.PROTECT)
    personnel= models.ForeignKey(Personnel, null=True, on_delete= models.PROTECT)
    

    class Meta:
        ordering = ('total_price' , '-update_time')

    def __str__(self):
        return f'{self.user} - {str(self.id)}'
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    quantity = models.IntegerField(default=1)
    
    # Foreign keys
    order = models.ForeignKey(Order, on_delete= models.CASCADE , related_name='item')
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
