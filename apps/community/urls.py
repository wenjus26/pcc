from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('category/<int:category_id>/', views.thread_list, name='thread_list'),
    path('category/<int:category_id>/new/', views.create_thread, name='create_thread'),
    path('thread/<int:pk>/', views.thread_detail, name='thread_detail'),
]
