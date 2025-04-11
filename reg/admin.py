from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,LGA,PollingUnit,State

# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['username', 'email', 'role', 'is_staff']
#     fieldsets = UserAdmin.fieldsets + (
#         ('Role Information', {'fields': ('role', 'phone_number', 'address')}),
#         ('Level-specific Information', {'fields': ('ward_name', 'local_govt_name', 'state_name')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         ('Role Information', {'fields': ('role', 'phone_number', 'address')}),
#         ('Level-specific Information', {'fields': ('ward_name', 'local_govt_name', 'state_name')}),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['fullname', 'username', 'email', 'is_superuser', 'email_verified', 'state', 'ward','lga','polling_unit']



@admin.register(PollingUnit)
class Polling(admin.ModelAdmin):
    list_display = ['name']


@admin.register(LGA)
class LocalAdmin(admin.ModelAdmin):
    list_display = ['name']