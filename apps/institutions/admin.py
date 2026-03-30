from django.contrib import admin
from .models import InstitutionProfile, Opportunity

@admin.register(InstitutionProfile)
class InstitutionProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'website', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('name', 'user__username')

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'institution')
    search_fields = ('title', 'description', 'institution__name')
    filter_horizontal = ('skills_required',)
