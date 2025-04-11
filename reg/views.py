



from django.shortcuts import render
from django.views import View


class RegView(View):
     def get(self, request):
        return render(request, 'reg/page-register-copy.html')
