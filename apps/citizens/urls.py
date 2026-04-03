from django.urls import path
from . import views

app_name = 'citizens'

urlpatterns = [
    path('talents/', views.talent_list, name='talent_list'),
    path('map/', views.skill_map, name='skill_map'),
    path('profile/register/', views.talent_register, name='talent_register'),
    path('profile/<uuid:uuid>/', views.profile_detail, name='profile_detail'),
    path('profile/<uuid:uuid>/edit/', views.profile_edit, name='profile_edit'),
    path('admin/download-template/', views.download_template, name='download_template'),
    path('admin/import-data/', views.import_data, name='import_data'),
]

