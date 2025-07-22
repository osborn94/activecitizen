from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os

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
    username = models.CharField(max_length=200, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=200, unique=False)
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
    image = models.ImageField(upload_to='user', height_field=None, width_field=None, max_length=None)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.fullname}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# === Image cleanup logic ===

@receiver(post_delete, sender=User)
def delete_user_image(sender, instance, **kwargs):
    if instance.image and instance.image.path and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

@receiver(pre_save, sender=User)
def delete_old_user_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New user

    try:
        old_user = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    old_image = old_user.image
    new_image = instance.image

    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
