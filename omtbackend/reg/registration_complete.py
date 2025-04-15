from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
import hashlib

User = get_user_model()

def generate_user_hash(user):
    uid = str(user.id)
    return hashlib.sha256(uid.encode()).hexdigest()

class Complete_Reg(View):
    template_name = 'reg/registration_complete.html'
    login_url = '/login/'

    def get(self, request, user_hash):
        if request.user.is_authenticated:
            expected_hash = generate_user_hash(request.user)
            if user_hash == expected_hash:
                context = self._get_context(request)
                return render(request, self.template_name, context)
            else:
                messages.error(request, "Invalid access. You cannot view this page.")
                return redirect(self.login_url)

        # Session fallback method
        session_hash = request.session.get('user_hash')
        if session_hash and session_hash == user_hash:
            for user in User.objects.all():
                if generate_user_hash(user) == user_hash:
                    context = self._get_context(request, user=user)
                    context['username'] = user.username
                    return render(request, self.template_name, context)

        messages.error(request, "Please log in to access this page.")
        return redirect(self.login_url)

    def _get_context(self, request, user=None):
        context = {}
        expected_ward_members = 10  # default threshold


        user = user or request.user

        if user and user.image:  # Ensure the user has an image
            user_image = user.image

            # If the user has an image, pass the image URL; otherwise, set it to None
            user_image_url = user.image.url if user.image else None


        # Use provided user or fallback to request.user
        user = user or request.user

        if user and user.ward:
            ward = user.ward

            # Count active and pending users in the same ward
            current_ward_members = User.objects.filter(ward=ward, email_verified=True).count()

            context.update({
                'current_ward_members': current_ward_members,
                'remaining_ward_members': max(expected_ward_members - current_ward_members, 0),
                'expected_ward_members': expected_ward_members,
                'ward_name': ward.name,
                'user_image_url': user.image.url if user.image else None  # Assuming `UserProfile` has `image` field
            })
        else:
            context.update({
                'ward_active_members': 0,
                'ward_pending_members': 0,
                'expected_ward_members': expected_ward_members,
                'ward_name': 'No Ward',
                'members_remaining': expected_ward_members,
                'user_image_url': None  # If no user or image is found
            })

        return context
