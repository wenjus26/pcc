from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('notifications/', views.notifications, name='notifications'),
    path('api/talent-locations/', views.talent_locations, name='talent_locations'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('contact/', views.contact, name='contact'),
]
