# django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

# third party imports
import datetime
import pytz

User = get_user_model()


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, entered_code=None):
        try:
            code = request.session["personnel_verify"]["code"]
            created_at = datetime.datetime.fromisoformat(
                request.session["personnel_verify"]["created_at"]
            )
            expired_time = datetime.datetime.now(
                tz=pytz.timezone("Asia/Tehran")
            ) - datetime.timedelta(minutes=1)
            if entered_code == code and created_at > expired_time:
                user = User.objects.get(phone_number=phone_number)
            else:
                return None
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id: int):
        try:
            user = User.objects.get(pk=user_id)
        except:
            return None
        return user
