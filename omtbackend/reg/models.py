from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
from django.conf import settings


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LGA(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Ward(models.Model):
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"



class PollingUnit(models.Model):
    name = models.CharField(max_length=200)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='polling_unit')
    telegram_group_link = models.URLField(blank=True, null=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['name', 'ward'], name='unique_pollingunit_per_ward')
        ]

    def __str__(self):
        return f"{self.name}"


ROLE_CHOICES = [
    ('member', 'Member'),
    ('ward_admin', 'Ward Admin'),
    ('lga_admin', 'LGA Admin'),
    ('state_admin', 'State Admin'),
    ('national_admin', 'National Admin'),
    ('secretary', 'Secretary'),
    ('treasurer', 'Treasurer'),
]

STATUS_CHOICES = [
    ('dormant', 'Dormant'),
    ('active', 'Active'),
]

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('Other', 'Other'),
)

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
    # approved_at = models.DateTimeField(null=True, blank=True)


    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='dormant')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    lga = models.ForeignKey(LGA, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    polling_unit = models.ForeignKey(PollingUnit, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='user', height_field=None, width_field=None, max_length=None)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.fullname}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class WardAdminNomination(models.Model):
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nominations')
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes_cast')
    ward = models.ForeignKey('Ward', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('target_user', 'voter')  # prevent duplicate votes from same person

    def __str__(self):
        return f"{self.voter.fullname} nominated {self.target_user.fullname}"


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
