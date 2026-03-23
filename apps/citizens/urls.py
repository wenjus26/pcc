from django.urls import path
from . import views

app_name = 'citizens'

urlpatterns = [
    path('talents/', views.talent_list, name='talent_list'),
    path('profile/<uuid:uuid>/', views.profile_detail, name='profile_detail'),
    path('profile/<uuid:uuid>/edit/', views.profile_edit, name='profile_edit'),
]

