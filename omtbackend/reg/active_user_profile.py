from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .models import LGA, State, Ward, PollingUnit
import hashlib
import traceback

User = get_user_model()

def generate_user_hash(user):
    uid = str(user.id)
    return hashlib.sha256(uid.encode()).hexdigest()

@method_decorator([login_required(login_url='/login/'), never_cache], name='dispatch')
class ActiveUserProfile(View):
    template_name = 'reg/active_user_profile.html'
    login_url = '/login/'

    def _get_context(self, request, user):
       """Build the context dictionary for the template."""
       context = {
           'user': user,
           'user_image_url': getattr(user.image, 'url', None),
           'user_ward': getattr(user, 'ward', None),
           'user_lga': getattr(user, 'lga', None),
           'user_polling_unit': getattr(user, 'polling_unit', None),
           'user_role': getattr(user, 'role', None),
           'user_phone': getattr(user, 'phone', None),
           'user_dob': getattr(user, 'dob', None),
           'user_name': getattr(user, 'username', ''),
           'user_fullname': getattr(user, 'fullname', ''),
           'user_email': getattr(user, 'email', '')
       }
       return context

    def dispatch(self, request, *args, **kwargs):
        """Validate hash for both GET and POST requests."""
        user_hash = kwargs.get('user_hash')
        if not request.user.is_authenticated:
            return redirect(self.login_url)

        expected_hash = generate_user_hash(request.user)
        if user_hash != expected_hash:
            print("Hash mismatch or invalid session.")
            return redirect(self.login_url)

        request.session['user_hash'] = expected_hash
        request.session['user_id'] = request.user.id
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_hash):
        context = self._get_context(request, request.user)
        context['expected_hash'] = user_hash
        return render(request, self.template_name, context)   

    