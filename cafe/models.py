from django.db import models
# Create your models here.

class Personnel(models.Model):
    pass

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

class Order(models.Model):
    table_name = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    total_price = models.FloatField()

    # Foreign keys
    customer = models.ForeignKey(Customer, on_delete= models.PROTECT)
    personnel= models.ForeignKey(Personnel, null=True, on_delete= models.PROTECT)

def item_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / <instance.__class__.__name__>_<id>/<filename>
    return '{2}_{0}/{1}'.format(instance.id, filename, instance.__class__.__name__)


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to = item_directory_path)

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to = item_directory_path)
    is_available = models.BooleanField(default= True)
    description = models.TextField()
    price = models.FloatField()

    # Foreign keys
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

class OrderItem(models.Model):
    quantity = models.IntegerField()
    
    # Foreign keys
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
