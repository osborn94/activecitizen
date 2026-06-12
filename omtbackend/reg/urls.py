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
from django.urls import reverse_lazy
from .waiting_room_form import WaitView
from .admin_dashboard import WardAdmin
from .active_user import ActiveUser, DormantUser
from .mem_manage import MemManage
from .pu_agent import PuAgent
from .pu_manage import PuManage
from .bar_chart import get_polling_unit_members
from .pie_chart import get_agents_per_pu
# from .userModal import UserDetailView

from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView
from .ward_admin_profile import WardAdminProfile
from .active_user_profile import ActiveUserProfile


urlpatterns = [

    path('', HomepageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('success/<str:user_hash>/', Complete_Reg.as_view(), name='success'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('next-step/', WaitView.as_view(), name='next_page'),
    path('ward_admin/<str:user_hash>/', WardAdmin.as_view(), name='ward_admin'),
    path('ward_admin_profile/<str:user_hash>/', WardAdminProfile.as_view(), name='ward_admin_profile'),
    path('mem_manage/<str:user_hash>/', MemManage.as_view(), name='mem_manage'),
    path('pu_agent/<str:user_hash>/', PuAgent.as_view(), name='pu_agent'),
    path('pu_manage/<str:user_hash>/', PuManage.as_view(), name='pu_manage'),
    path('active_user/<str:user_hash>/', ActiveUser.as_view(), name='active_user'),

    path('active_user_profile/<str:user_hash>/', ActiveUserProfile.as_view(), name='active_user_profile'),

    path('get-polling-unit-members/', get_polling_unit_members, name='get_polling_unit_members'),
    path('get-agents-per-pu/', get_agents_per_pu, name='get_agents_per_pu'),


    path('dormant_user/<str:user_hash>/', DormantUser.as_view(), name='dormant_user'),

    # path('reset-password/', auth_views.PasswordResetView.as_view(
    #     template_name='reg/password_reset.html',
    #     email_template_name='reg/password_reset_email.html',
    # ), name='password_reset'),
    path('reset-password/', CustomPasswordResetView.as_view(), name='password_reset'),

    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='reg/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reg/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='reg/password_reset_complete.html'), name='password_reset_complete'),

 

    # path('get-user/<str:user_id>/', UserDetailView.as_view(), name='get_user_details')


] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
