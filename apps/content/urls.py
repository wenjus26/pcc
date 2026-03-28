from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('programme-societe/', views.programme_societe, name='programme_societe'),
    path('galerie/', views.gallery, name='gallery'),
    path('romuald-wadagni/', views.biography, name='biography'),
    path('contributions/', views.contributions, name='contributions'),
]

