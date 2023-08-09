from django.core.management.base import BaseCommand
from accounts.models import OTPCode
import datetime
import pytz


class Command(BaseCommand):
    help = "Delete expired otps!"

    def handle(self, *args, **options):
        expired_time = datetime.datetime.now(
            tz=pytz.timezone("Asia/Tehran")
        ) - datetime.timedelta(minutes=1)
        OTPCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write("all expired otp codes has been removed!")
