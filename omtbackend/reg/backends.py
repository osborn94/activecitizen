from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"Authenticating user: {username}")
        if username is None:
            return None

        try:
            user = User.objects.get(Q(email__iexact=username.strip()))
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None

