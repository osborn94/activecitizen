from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import PasswordResetView

class RegView(View):
     def get(self, request):
        return render(request, 'reg/page-register-copy.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'reg/password_reset.html'
    html_email_template_name = 'reg/password_reset_email.html'
   #  subject_template_name = 'reg/password_reset_subject.txt'
