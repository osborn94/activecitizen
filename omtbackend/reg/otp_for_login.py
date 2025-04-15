import random
from django.utils import timezone
from .register import send_otp_email


def send_otp_to_user(user, request):
    otp_code = str(random.randint(100000, 999999))

    # Save OTP and timestamp to the user model
    user.otp = otp_code
    user.otp_created_at = timezone.now()
    user.save()

    # Send the OTP email
    send_otp_email(user, otp_code, request)