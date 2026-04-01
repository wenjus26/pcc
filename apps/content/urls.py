from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('events/', views.event_list, name='event_list'),
    path('events/<uuid:uuid>/', views.event_detail, name='event_detail'),
    path('programme-societe/', views.programme_societe, name='programme_societe'),
    path('galerie/', views.gallery, name='gallery'),
    path('romuald-wadagni/', views.biography, name='biography'),
    path('contributions/', views.contributions, name='contributions'),
    path('videos/', views.video_list, name='video_list'),
]

