from django.db import models
from utils import item_directory_path

# Create your models here.

class Personnel(models.Model):
    pass

class Customer(models.Model):
    name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=20, unique=True)




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

