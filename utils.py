from kavenegar import *


def item_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / <instance.__class__.__name__>_<id>/<filename>
    return "{2}_{0}/{1}".format(instance.id, filename, instance.__class__.__name__)


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
