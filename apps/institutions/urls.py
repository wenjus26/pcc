from django.urls import path
from . import views

app_name = 'institutions'

urlpatterns = [
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('opportunities/create/', views.opportunity_create, name='opportunity_create'),
    path('opportunities/<uuid:uuid>/', views.opportunity_detail, name='opportunity_detail'),
    path('opportunities/<uuid:uuid>/edit/', views.opportunity_edit, name='opportunity_edit'),
]

