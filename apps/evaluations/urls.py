from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('list/', views.evaluation_list, name='evaluation_list'),
    path('take/<uuid:uuid>/', views.take_evaluation, name='take_evaluation'),
    path('result/<int:pk>/', views.evaluation_result, name='evaluation_result'),
]
