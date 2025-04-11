
from django.shortcuts import render, redirect
from django.urls import reverse
# from django.views import View
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# import pyotp

User = get_user_model()

class LoginView(View):
    def get(self, request):
        return render(request, 'reg/page-login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exists():
            return JsonResponse({"error": "User does not exist"}, status=400)

        user = authenticate(request, email=email, password=password)
        
        if user is None:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
        
        if not user.email_verified:
            return JsonResponse({"email": "account not active"}, status=400)
        
        # Log the user in
        login(request, user)
        
        # Return success response
        next_url = request.POST.get('next', reverse('dashboard'))
        return JsonResponse({
            "success": True,
            "message": f"Welcome back, {user.username}!",
            "redirect_url": next_url
        })