from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import LGA,State,Ward,PollingUnit

User = get_user_model()
class RegisterView(View):
    
    def get(self, request):
        return render(request, 'reg/page-register.html')
    
    def post(self, request):
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')  
        mobile_number = request.POST.get('mobile_number')
        state_name = request.POST.get('state')
        lga_name = request.POST.get('lga')
        ward_name = request.POST.get('ward')
        polling_unit_name = request.POST.get('polling_unit')
        passport = request.FILES.get('passport')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate required fields
        if not all([full_name, username, email, mobile_number, password, confirm_password, state_name, lga_name, ward_name, polling_unit_name,passport]):
            return JsonResponse({'error': 'Please fill all the form fields'}, status=400)
        
     
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(phone=mobile_number).exists():
            return JsonResponse({'error': 'Phone number already exists'}, status=400)
        
        try:
            state, _ = State.objects.get_or_create(name=state_name)
            lga, _ = LGA.objects.get_or_create(name=lga_name, state=state)
            ward, _ = Ward.objects.get_or_create(name=ward_name, lga=lga)
            polling_unit, _ = PollingUnit.objects.get_or_create(
                name=polling_unit_name, 
                ward=ward
              # Set default values if creating new
            )
            
            user = User.objects.create(
                fullname=full_name,
                username=username,
                email=email,
                phone=mobile_number,
                state=state,
                lga=lga,
                ward=ward,
                polling_unit=polling_unit,
                password=make_password(password),
                image=passport,
               
            )
            
            return JsonResponse({'success': 'User registered successfully!'}, status=200)
            
        except State.DoesNotExist:
            return JsonResponse({'error': 'Invalid state selected'}, status=400)
        except LGA.DoesNotExist:
            return JsonResponse({'error': 'Invalid LGA selected'}, status=400)
        except Ward.DoesNotExist:
            return JsonResponse({'error': 'Invalid ward selected'}, status=400)
        except PollingUnit.DoesNotExist:
            return JsonResponse({'error': 'Invalid polling unit selected'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)