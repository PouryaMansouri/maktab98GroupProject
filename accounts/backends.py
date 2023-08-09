from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


User = get_user_model()


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None):
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id: int):
        try:
            user = User.objects.get(pk=user_id)
        except:
            return None
        return user
