from typing import Any
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class PersonnelManager(BaseUserManager):
    def create_user(self, full_name, email, phone_number, image, password):
        if not full_name:
            raise ValidationError("User have to have full name!")
        if not email:
            raise ValidationError("User have to have email!")
        if not phone_number:
            raise ValidationError("User have to have phone_number!")

        user = self.model(
            full_name=full_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            image=image,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, phone_number, image, password):
        user = self.create_user(full_name, email, phone_number, image, password)
        user.is_admin = True
        user.save(using=self._db)
        return user