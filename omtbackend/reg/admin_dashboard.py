from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import PollingUnit
import hashlib
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

User = get_user_model()

def generate_user_hash(user):
    """Generate a SHA-256 hash of the user ID."""
    uid = str(user.id)
    return hashlib.sha256(uid.encode()).hexdigest()


@method_decorator([login_required(login_url='/login/'), never_cache], name='dispatch')
class WardAdmin(View):
    template_name = 'reg/ward_admin.html'
    login_url = '/login/'

    def _get_context(self, request, user):
        """Build the context dictionary for the template."""
        context = {
            'user': user,
            'user_image_url': getattr(user.image, 'url', None),
            'user_ward': getattr(user, 'ward', None),
            'user_name': getattr(user, 'username', ''),
            'user_fullname': getattr(user, 'fullname', ''),
            'user_gender': getattr(user, 'gender', ''),
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

    def post(self, request, user_hash):
        action = request.POST.get('action')
        if action == 'edit_member':
            member_id = request.POST.get('member_id')
            fullname = request.POST.get('fullname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            # polling_unit = request.POST.get('polling_unit')

            try:
                member = User.objects.get(id=member_id)
                member.fullname = fullname
                member.username = username
                member.gender = gender
                member.email = email
                # member.polling_unit = polling_unit
                if phone:
                    member.phone = phone
                # Optionally handle polling_unit here if applicable
                member.save()
            except User.DoesNotExist:
                return JsonResponse({'error': 'Member not found'}, status=404)

        elif action == 'delete_member':
            member_id = request.POST.get('member_id')
            try:
                member = User.objects.get(id=member_id)
                member.delete()
            except User.DoesNotExist:
                return JsonResponse({'error': 'Member not found'}, status=404)        

        context = self._get_context(request, request.user)
        context['expected_hash'] = user_hash
        return render(request, self.template_name, context)
