from django.urls import path
from . import views

app_name = 'institutions'

urlpatterns = [
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('opportunities/<uuid:uuid>/', views.opportunity_detail, name='opportunity_detail'),
]

