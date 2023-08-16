from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import PersonnelManager


# Create your models here.
class Personnel(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11, unique=True)
    image = models.ImageField(upload_to="personnel/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = PersonnelManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "full_name"]

    def __str__(self):
        return self.email

    def has_perm(user_obj, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Customer(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.phone_number}"

