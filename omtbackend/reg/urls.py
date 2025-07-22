from django.urls import path
from .views import RegView
from .register import RegisterView
from .login import LoginView
from .home import HomepageView
from .registration_complete import Complete_Reg
from .verify_otp import VerifyOTPView, ResendOTPView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('home/', HomepageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
      path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('success/<str:user_hash>/', Complete_Reg.as_view(), name='success'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
