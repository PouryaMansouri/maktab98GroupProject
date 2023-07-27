from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Order(models.Model):
    table_name = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    total_price_= models.FloatField()

    # Foreign keys
    customer = models.ManyToManyField(User, through= 'OrderItem')
    personnel= models.ManyToManyField(User, through='OrderItem', null=True)
