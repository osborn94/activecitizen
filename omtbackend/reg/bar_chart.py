from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from .models import PollingUnit

@login_required
def get_polling_unit_members(request):
    user_ward = request.user.ward

    if not user_ward:
        return JsonResponse({'labels': [], 'data': []})  # No ward assigned

    polling_units = (
        PollingUnit.objects
        .filter(ward=user_ward)
        .annotate(
            member_count=Count('user', filter=Q(user__role='member', user__status='active'))
        )
        .values('name', 'member_count')
    )

    labels = [pu['name'] for pu in polling_units]
    data = [pu['member_count'] for pu in polling_units]

    return JsonResponse({'labels': labels, 'data': data})
