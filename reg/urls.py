from django.urls import path
from .views import RegView
from .register import RegisterView
from .login import LoginView
from .dashboard import HomepageView
from .registration_complete import Complete_Reg

urlpatterns = [

    path('dashboard/', HomepageView.as_view(), name='dashboard'),

    path('register/', RegisterView.as_view(), name='register'),
  
    path('login/', LoginView.as_view(), name='login'),
      path('success/', Complete_Reg.as_view(), name='success'),

]
