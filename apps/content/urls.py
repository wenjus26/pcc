from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('blog/', views.post_list, name='post_list'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('events/', views.event_list, name='event_list'),
]

