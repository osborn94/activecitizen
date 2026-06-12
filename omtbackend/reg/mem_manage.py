from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
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
class MemManage(View):
    template_name = 'reg/members.html'
    login_url = '/login/'

    def _get_context(self, request, user):
        context = {
            'user': user,
            'user_image_url': getattr(user.image, 'url', None),
            'user_ward': getattr(user, 'ward', None),
            'user_name': getattr(user, 'username', ''),
            'user_fullname': getattr(user, 'fullname', ''),
            'user_email': getattr(user, 'email', ''),
            'user_gender': getattr(user, 'gender', '')

            # 'states': State.objects.all(),
            # 'lgas': LGA.objects.filter(state=user.state) if user.state else [],
            # 'wards': Ward.objects.filter(lga=user.lga) if user.lga else [],
            # 'polling_units': PollingUnit.objects.filter(ward=user.ward) if user.ward else [],
        }

        ward = user.ward
        if ward:
            context['total_ward_members'] = User.objects.filter(ward=ward, email_verified=True).count()
            context['total_polling_units'] = PollingUnit.objects.filter(ward=ward).count()
            context['active_agents'] = User.objects.filter(ward=ward, status="active").count()
            context['pending_agents'] = User.objects.filter(ward=ward, status="dormant", email_verified=True).count()
            context['pending_members'] = User.objects.filter(ward=ward, status="dormant", email_verified=True)
            context['approved_members'] = User.objects.filter(ward=ward, email_verified=True, status='active')

        return context

    def dispatch(self, request, *args, **kwargs):
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
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            try:
                member = User.objects.get(id=member_id)
                member.fullname = fullname
                member.email = email
                if phone:
                    member.phone = phone
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

        elif action == 'approve_member':
            member_id = request.POST.get('member_id')
            try:
                member = User.objects.get(id=member_id)
                member.status = 'active'
                member.save()
                return JsonResponse({'success': 'Member approved'})
            except User.DoesNotExist:
                return JsonResponse({'error': 'Member not found'}, status=404)

        elif action == 'register_member':
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            username = request.POST.get('username')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            state_name = request.POST.get('state')
            lga_name = request.POST.get('lga')
            ward_name = request.POST.get('ward')
            polling_unit_name = request.POST.get('polling_unit')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            passport = request.FILES.get('passport')

            if not all([fullname, email, phone, username, password, confirm_password, state_name, lga_name, ward_name, polling_unit_name, passport, gender, dob]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already taken.'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already in use.'}, status=400)

            if User.objects.filter(phone=phone).exists():
                return JsonResponse({'error': 'Phone number already exists'}, status=400)

            try:
                # state = State.objects.get(id=state_id)
                # lga = LGA.objects.get(id=lga_id, state=state)
                # ward = Ward.objects.get(id=ward_id, lga=lga)
                # polling_unit = PollingUnit.objects.get(id=polling_unit_id, ward=ward)

                # state = State.objects.get(name__iexact=state_name.strip())
                # lga = LGA.objects.get(name__iexact=lga_name.strip(), state=state)
                # ward = Ward.objects.get(name__iexact=ward_name.strip(), lga=lga)
                # polling_unit = PollingUnit.objects.get(name__iexact=polling_unit_name.strip(), ward=ward)

                state, _ = State.objects.get_or_create(name=state_name)
                lga, _ = LGA.objects.get_or_create(name=lga_name, state=state)
                ward, _ = Ward.objects.get_or_create(name=ward_name, lga=lga)
                polling_unit, _ = PollingUnit.objects.get_or_create(name=polling_unit_name, ward=ward)


                user = User.objects.create_user(
                    username=username,
                    email=email,
                    fullname=fullname,
                    phone=phone,
                    ward=request.user.ward,  # Keep ward same as admin's
                    status='dormant',
                    email_verified=False,
                    state=state,
                    lga=lga,
                    polling_unit=polling_unit,
                    password=password,
                    image=passport,
                    is_active=False,
                    dob=dob,
                    gender=gender,
                )
                return JsonResponse({'success': 'Member registered successfully'})
            except (State.DoesNotExist, LGA.DoesNotExist, Ward.DoesNotExist, PollingUnit.DoesNotExist):
                return JsonResponse({'error': 'Invalid location selection.'}, status=400)
            except Exception as e:
                traceback.print_exc()
                return JsonResponse({'error': str(e)}, status=500)

        context = self._get_context(request, request.user)
        context['expected_hash'] = user_hash
        return render(request, self.template_name, context)

