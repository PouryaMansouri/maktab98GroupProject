from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Order(models.Model):
    table_name = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    total_price_= models.FloatField()

    # Foreign keys
    customer = models.ManyToManyField(User)
    personnel= models.ManyToManyField(User)

class Category(models.Model):
    pass

def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / product_<id>/<filename>
    return 'product_{0}/{1}'.format(instance.id, filename)

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to = product_directory_path)
    is_available = models.BooleanField(default= True)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

class OrderItem(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
