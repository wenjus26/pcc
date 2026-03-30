from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_verified')
    list_filter = ('role', 'is_staff', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('Platform Info', {'fields': ('role', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Platform Info', {'fields': ('role', 'is_verified')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
