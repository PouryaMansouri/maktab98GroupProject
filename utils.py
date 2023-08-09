from kavenegar import *

from django.db.models import Max

def item_directory_path(instance, filename):
    # Because before create a category it does not have any id
    # so need to get next availabe id from db
    # also, instance has not access to its class, so use __class__:

    items = instance.__class__.objects.all()
    #might be possible model has no records so make instance.__class__ to handle None
    next_id = items.aggregate(Max('id'))['id__max'] + 1 if items else 1
    # file will be uploaded to MEDIA_ROOT / <instance.__class__.__name__>_<id>/<filename>
    return '{2}/{2}_{0}/{1}'.format(next_id, filename, instance.__class__.__name__)


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI("Your APIKey", timeout=20)
        params = {
            "sender": "",  # optional
            "receptor": phone_number,  # multiple mobile number, split by comma
            "message": f"Your code is {code}",
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
