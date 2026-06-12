from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
# from .models import Ward
from .models import PollingUnit

@login_required
def get_agents_per_pu(request):
    user_ward = request.user.ward

    if not user_ward:
        return JsonResponse({'labels': [], 'data': []}) 

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


    # agents_data = (
    #     Ward.objects
    #     .annotate(
    #         agent_count=Count('pollingunit__user', filter=Q(pollingunit__user__role='agent', pollingunit__user__status='active'))
    #     )
    #     .values('name', 'agent_count')
    # )

    # labels = [ward['name'] for ward in agents_data]
    # data = [ward['agent_count'] for ward in agents_data]

    # return JsonResponse({'labels': labels, 'data': data})
