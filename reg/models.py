from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField



class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LGA(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.state.name})"


class Ward(models.Model):
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.lga.name})"


class PollingUnit(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    telegram_group_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.ward.name})"

    
ROLE_CHOICES = [
        ('supporter', 'Supporter'),
        ('ward_admin', 'Ward Admin'),
        ('lga_admin', 'LGA Admin'),
        ('state_admin', 'State Admin'),
        ('national_admin', 'National Admin'),
    ]

STATUS_CHOICES = [
        ('dormant', 'Dormant'),
        ('active', 'Active'),
    ]

class User(AbstractUser):
    id = ShortUUIDField(
        primary_key=True, 
        unique=True, 
        editable=False, 
        alphabet='bcarem12345qop09867890'
    )
    fullname = models.CharField(max_length=200, default=False)
    username = models.CharField(max_length=200, unique=True)
    phone = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='supporter')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='dormant')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    lga = models.ForeignKey(LGA, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    polling_unit = models.ForeignKey(PollingUnit, on_delete=models.SET_NULL, null=True, blank=True)
    image =  models.ImageField( upload_to='user', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return f"{self.fullname}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
  
   

 
# class WardAccount(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='wardaccount')
#     date_of_birth = models.DateField()
#     image = models.ImageField( upload_to='profile')

#     def __str__(self):
#         return self.user.fullname
    

# class LocalAccount(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='localaccount')
#     date_of_birth = models.DateField()
#     registration_number = models.CharField(max_length=200)
#     address = models.TextField()


#     def __str__(self):
#         return self.user.fullname
    

# class StateAccount(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='stateaccount')
#     date_of_birth = models.DateField()
#     registration_number = models.CharField(max_length=200)
#     address = models.TextField()


#     def __str__(self):
#         return self.user.fullname


# class NationalAccount(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='nationalaccount')
#     date_of_birth = models.DateField()
#     registration_number = models.CharField(max_length=200)
#     address = models.TextField()


#     def __str__(self):
#         return self.user.fullname

