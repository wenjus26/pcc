from django.contrib import admin
from .models import Application, Match

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('citizen', 'opportunity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('citizen__user__username', 'opportunity__title')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('citizen', 'opportunity', 'score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('citizen__user__username', 'opportunity__title')
