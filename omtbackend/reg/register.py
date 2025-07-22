from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils import timezone
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.db.models import Count
from .models import LGA, State, Ward, PollingUnit
import threading
import six
import logging
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator

logger = logging.getLogger(__name__)


User = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()

# Email thread for sending asynchronous emails
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_otp_email(user, otp, request):
    """Send OTP verification email to user"""
    email_subject = 'Verify Your Email'
    email_body = render_to_string('reg/otp_verification_email.html', {
        'user': user,
        'otp': otp,
    })

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[user.email]
    )
    email.content_subtype = "html"
    EmailThread(email).start()


    
class RegisterView(View):
    def get(self, request):
        return render(request, 'reg/page-register.html')

    def post(self, request):
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        mobile_number = request.POST.get('mobile_number')
        state_name = request.POST.get('state')
        lga_name = request.POST.get('lga')
        ward_name = request.POST.get('ward')
        polling_unit_name = request.POST.get('polling_unit')
        passport = request.FILES.get('passport')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([full_name, email, username, mobile_number, password, confirm_password, state_name, lga_name, ward_name, polling_unit_name, passport]):
            return JsonResponse({'error': 'Please fill all the form fields'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        if User.objects.filter(phone=mobile_number).exists():
            return JsonResponse({'error': 'Phone number already exists'}, status=400)

        try:
            state, _ = State.objects.get_or_create(name=state_name)
            lga, _ = LGA.objects.get_or_create(name=lga_name, state=state)
            ward, _ = Ward.objects.get_or_create(name=ward_name, lga=lga)
            polling_unit, _ = PollingUnit.objects.get_or_create(name=polling_unit_name, ward=ward)

            otp = get_random_string(6, allowed_chars='0123456789')

            user = User.objects.create(
                fullname=full_name,
                username=username,
                email=email.lower(),
                phone=mobile_number,
                state=state,
                lga=lga,
                ward=ward,
                polling_unit=polling_unit,
                password=make_password(password),
                image=passport,
                is_active=False,
                otp=otp,
                otp_created_at=timezone.now(),
                email_verified=False
            )

            send_otp_email(user, otp, request)
            request.session['verification_user_id'] = user.id

            return JsonResponse({
                'success': 'Registration successful! Please check your email for verification code.',
                'redirect': reverse('verify_otp')
            })

        except Exception as e:
            logger.exception("Registration failed")
            return JsonResponse({'error': 'Something went wrong during registration.'}, status=500)


        
# class ActivateAccountView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None

#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.save()
            
#             # Count users in the same polling unit
#             polling_unit_members_count = User.objects.filter(
#                 polling_unit=user.polling_unit,
#                 is_active=True
#             ).count()
            
#             messages.success(request, 'Your account has been activated successfully!')
            
#             # Get ward information for the user
#             ward = user.ward
            
#             # Count active and total users in the ward
#             ward_active_members = User.objects.filter(
#                 ward=ward,
#                 is_active=True
#             ).count()
            
#             # For pending members, count inactive users or users awaiting approval
#             ward_pending_members = User.objects.filter(
#                 ward=ward,
#                 is_active=False
#             ).count()
            
#             # Expected members threshold (adjust as needed)
#             expected_ward_members = 10
            
#             # Redirect based on ward member count
#             if ward_active_members < expected_ward_members:
#                 # Pass these counts to the recruitment page
#                 request.session['ward_active_members'] = ward_active_members
#                 request.session['ward_pending_members'] = ward_pending_members
#                 request.session['expected_ward_members'] = expected_ward_members
#                 request.session['ward_name'] = ward.name
                
#                 return redirect('success')
#             else:
#                 return redirect('login')
#         else:
#             messages.error(request, 'Activation link is invalid or has expired!')
#             return redirect('register')
        