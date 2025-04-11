

from django.shortcuts import render
from django.views import View


class Complete_Reg(View):
     def get(self, request):
        return render(request, 'reg/registration_complete.html')
