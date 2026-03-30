from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/talent-locations/', views.talent_locations, name='talent_locations'),
]
