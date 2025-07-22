from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, get_user_model
from .registration_complete import generate_user_hash
from .otp_for_login import send_otp_to_user
from django.contrib.auth.hashers import check_password
import logging

logger = logging.getLogger(__name__)

User = get_user_model()



class LoginView(View):

    def get(self, request):
        return render(request, 'reg/page-login.html')
    

    def post(self, request):
        try:
            email = request.POST.get("email", "").strip().lower()
            password = request.POST.get("password")

            if not email or not password:
                return JsonResponse({"error": "Email and password are required."}, status=400)

            # Use authenticate to check credentials
            user = authenticate(request, username=email, password=password)

            if user is None:
                return JsonResponse({"error": "Invalid credentials"}, status=400)

            if not user.email_verified:
                # Store user ID in session for OTP verification
                request.session['verification_user_id'] = user.id
                send_otp_to_user(user, request)

                # Send response with redirect to verify OTP page
                return JsonResponse({
                    "success": False,
                    "error": "Email not verified. OTP has been sent to your email.",
                    "redirect_url": reverse('verify_otp')
                }, status=403)

            # Log user in (this sets the correct backend automatically)
            login(request, user)

            # Create user hash for session and store it
            user_hash = generate_user_hash(user)
            request.session['user_hash'] = user_hash
            request.session.save()

            # Redirect to success page or wherever is appropriate
            return JsonResponse({
                "success": True,
                "message": f"Welcome back, {user.username}!",
                "redirect_url": reverse('success', kwargs={'user_hash': user_hash})
            })

        except Exception as e:
            print("Login error:", e)
            return JsonResponse({"error": "Something went wrong. Please try again."}, status=500)
  
