from django.contrib import admin
from django.utils.html import format_html
from .models import User, LGA, PollingUnit, State, Ward


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['fullname', 'username', 'email', 'role', 'status', 'is_superuser', 'email_verified', 'state', 'ward', 'lga', 'polling_unit', 'image_preview']
    readonly_fields = ['image_preview']
    list_filter = ['role', 'status', 'state', 'lga']
    search_fields = ['fullname', 'email', 'username', 'phone']
    
    # Optimized foreign key lookups for large related tables
    autocomplete_fields = ['state', 'lga', 'ward', 'polling_unit']

    def get_queryset(self, request):
        # Optimize DB hits using select_related
        return super().get_queryset(request).select_related(
            'state', 'lga', 'ward', 'polling_unit'
        )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:4px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Profile Image"


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']  # Needed for autocomplete


@admin.register(LGA)
class LocalAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']
    list_filter = ['state']
    search_fields = ['name']


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['name', 'lga']
    list_filter = ['lga']
    search_fields = ['name']


@admin.register(PollingUnit)
class Polling(admin.ModelAdmin):
    list_display = ['name', 'ward']
    list_filter = ['ward']
    search_fields = ['name']


























# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User,LGA,PollingUnit,State



# @admin.register(User)
# class AdminUser(admin.ModelAdmin):
#     list_display = ['fullname', 'username', 'email', 'is_superuser', 'email_verified', 'state', 'ward','lga','polling_unit']



# @admin.register(PollingUnit)
# class Polling(admin.ModelAdmin):
#     list_display = ['name']


# @admin.register(LGA)
# class LocalAdmin(admin.ModelAdmin):
#     list_display = ['name']