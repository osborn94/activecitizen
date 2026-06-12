from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import WardAdminNomination 

User = get_user_model()

@method_decorator(login_required, name='dispatch')
class WaitView(View):

    def get(self, request):
        return render(request, 'reg/waitRoomForm.html')

    def post(self, request):
        username = request.POST.get('username')
        voter = request.user

        if not username:
            return JsonResponse({'success': False, 'error': 'Please fill in the username field.'}, status=400)

        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'No user found with that username.'}, status=404)

        # Ensure both users are in the same ward
        if not voter.ward or voter.ward != target_user.ward:
            return JsonResponse({'success': False, 'error': 'User is not in the same ward as you.'}, status=403)

        # Prevent duplicate nominations
        if WardAdminNomination.objects.filter(target_user=target_user, voter=voter).exists():
            return JsonResponse({'success': False, 'error': 'You have already nominated this user.'}, status=400)
            
        # Check if voter has already nominated someone else in the same ward
        if WardAdminNomination.objects.filter(voter=voter, ward=voter.ward).exclude(target_user=target_user).exists():
            return JsonResponse({'success': False, 'error': 'You have already nominated someone else in this ward.',"redirect_url":"/home/"}, status=400)   

        # Save the nomination
        WardAdminNomination.objects.create(target_user=target_user, voter=voter, ward=voter.ward)

        # Count total nominations for this user in the ward
        total_votes = WardAdminNomination.objects.filter(target_user=target_user, ward=voter.ward).count()
        threshold = 2

        if total_votes >= threshold:
            target_user.role = 'ward_admin'
            target_user.status = 'active'
            target_user.save()

            # Clean up nominations after promotion
            WardAdminNomination.objects.filter(target_user=target_user, ward=voter.ward).delete()

            return JsonResponse({
                'success': True,
                'message': f"{target_user.fullname} has been promoted to Ward Admin!",
                'redirect_url': '/home/'  # Optional redirect after promotion
            })

        votes_remaining = threshold - total_votes
        return JsonResponse({
            'success': True,
            'message': f"Nomination added. {votes_remaining} more needed to promote {target_user.fullname}.",
            'redirect_url': '/home/'
        })
