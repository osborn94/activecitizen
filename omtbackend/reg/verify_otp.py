import logging
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model, login
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse
from hmac import compare_digest
from django.utils.crypto import get_random_string
from .registration_complete import generate_user_hash
from .register import send_otp_email

logger = logging.getLogger(__name__)
User = get_user_model()

OTP_EXPIRY_MINUTES = 10

class VerifyOTPView(View):
    def get(self, request):
        user_id = request.session.get('verification_user_id')
        if not user_id:
            logger.warning("No verification session found.")
            return render(request, 'reg/otp_page.html', {'error': 'No verification session found'})
        return render(request, 'reg/otp_page.html')

    def post(self, request):
        user_id = request.session.get('verification_user_id')
        entered_otp = request.POST.get('otp')

        if not user_id or not entered_otp:
            logger.warning("Invalid verification attempt: Missing user ID or OTP.")
            return JsonResponse({'success': False, 'error': 'Invalid verification attempt.'}, status=400)

        try:
            user = User.objects.get(id=user_id)

            # Debug logs to verify user information
            logger.info(f"User found: {user.username}, Email Verified: {user.email_verified}, OTP: {user.otp}")

            if user.email_verified:
                logger.info("User email is already verified.")
                return JsonResponse({'success': True, 'message': 'Email already verified.'}, status=200)

            if timezone.now() > user.otp_created_at + timedelta(minutes=OTP_EXPIRY_MINUTES):
                logger.info("OTP has expired.")
                return JsonResponse({'success': False, 'error': 'OTP expired.', 'expired': True}, status=400)

            if not compare_digest(str(user.otp), str(entered_otp)):
                logger.info(f"Invalid OTP entered: {entered_otp}")
                return JsonResponse({'success': False, 'error': 'Invalid OTP.', 'invalid': True}, status=400)

            # Mark the user as verified
            user.is_active = True
            user.email_verified = True
            user.otp = None  # Clear the OTP after verification
            user.otp_created_at = None  # Clear the OTP creation time
            user.save()

            # Log user in
            backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=backend)

            # Create session hash and store it
            user_hash = generate_user_hash(user)
            request.session['user_hash'] = user_hash
            request.session.pop('verification_user_id', None)

            logger.info(f"User {user.username} successfully verified and logged in.")

            return JsonResponse({
                'success': True,
                'message': 'Verification successful!',
                'redirect_url': reverse('success', kwargs={'user_hash': user_hash})
            })

        except User.DoesNotExist:
            logger.error("User not found.")
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            logger.exception("Verification failed: Unexpected error")
            return JsonResponse({'error': 'Something went wrong during verification. Please try again later.'}, status=500)



class ResendOTPView(View):
    def get(self, request):
        user_id = request.session.get('verification_user_id')
        if not user_id:
            return JsonResponse({'error': 'No verification session found.'}, status=400)

        try:
            user = User.objects.get(id=user_id)

            cooldown = timedelta(minutes=1)
            if user.otp_created_at and timezone.now() - user.otp_created_at < cooldown:
                return JsonResponse({'error': 'Please wait before requesting a new code.'}, status=429)

            new_otp = get_random_string(6, allowed_chars='0123456789')
            user.otp = new_otp
            user.otp_created_at = timezone.now()
            user.save()

            send_otp_email(user, new_otp, request)

            return JsonResponse({'success': True, 'message': 'OTP resent successfully.'})

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception:
            logger.exception("Resend OTP failed")
            return JsonResponse({'error': 'Something went wrong. Try again.'}, status=500)
