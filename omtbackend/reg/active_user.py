from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
import hashlib
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import PollingUnit

User = get_user_model()


def generate_user_hash(user):
    uid = str(user.id)
    return hashlib.sha256(uid.encode()).hexdigest()

@method_decorator([login_required(login_url='/login/'), never_cache], name='dispatch')
class ActiveUser(View):
    template_name = 'reg/active_user.html'
    login_url = '/login/'

    def _get_context(self, request, user):
        """Build the context dictionary for the template."""
        context = {
            'user': user,
            'user_image_url': getattr(user.image, 'url', None),
            'user_ward': getattr(user, 'ward', None),
            'user_name': getattr(user, 'username', ''),
            'user_fullname': getattr(user, 'fullname', ''),
            'user_role': getattr(user, 'role', ''),
            'user_gender': getattr(user, 'gender', ''),
            'user_dob': getattr(user, 'dob', ''),
            'user_email': getattr(user, 'email', '')
        }

        ward = user.ward
        if ward:
            context['total_ward_members'] = User.objects.filter(ward=ward, email_verified=True).count()
            context['total_polling_units'] = PollingUnit.objects.filter(ward=ward).count()
            context['active_agents'] = User.objects.filter(ward=ward, status="active").count()
            context['pending_agents'] = User.objects.filter(ward=ward, status="dormant", email_verified=True).count()
            context['approved_members'] = User.objects.filter(ward=ward, email_verified=True, status='active')
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












class DormantUser(View):
    template_name = 'reg/dormant_user.html'
    login_url = '/login/'

    def get(self, request, user_hash):
        if request.user.is_authenticated:
            expected_hash = generate_user_hash(request.user)
            if user_hash == expected_hash:
                # context = self._get_context(request)
                return render(request, self.template_name)
            else:
                messages.error(request, "Invalid access. You cannot view this page.")
                return redirect(self.login_url)

        # Session fallback method
        session_hash = request.session.get('user_hash')
        if session_hash and session_hash == user_hash:
            for user in User.objects.all():
                if generate_user_hash(user) == user_hash:
                    # context = self._get_context(request, user=user)
                    # context['username'] = user.username
                    return render(request, self.template_name, context)

        messages.error(request, "Please log in to access this page.")
        return redirect(self.login_url)
        # return render(request, 'reg/dormant_user.html')

