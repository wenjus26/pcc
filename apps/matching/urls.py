from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('apply/<uuid:uuid>/', views.apply_to_opportunity, name='apply_to_opportunity'),
]
