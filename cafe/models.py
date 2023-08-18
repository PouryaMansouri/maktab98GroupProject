# django imports
from django.db import models

# inner modules imports
from utils import item_directory_path


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=item_directory_path)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=item_directory_path)
    is_available = models.BooleanField(default=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Foreign keys
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name
