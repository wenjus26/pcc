from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('mon-espace/', views.dashboard, name='dashboard'),
    
    # Administration PCC
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/profile/<uuid:uuid>/', views.admin_profile_detail, name='admin_profile_detail'),
    path('admin/profile/<uuid:uuid>/validate/', views.validate_profile, name='validate_profile'),
    path('admin/match/', views.admin_match_talent, name='admin_match_talent'),
    path('admin/export/talents/', views.export_talents_excel, name='export_talents'),
    path('admin/validate-all-profiles/', views.admin_validate_all_profiles, name='admin_validate_all_profiles'),

    
    # Création Admin
    path('admin/create/event/', views.admin_create_event, name='admin_create_event'),
    path('admin/create/institution/', views.admin_create_institution, name='admin_create_institution'),
    path('admin/create/citizen/', views.admin_create_citizen, name='admin_create_citizen'),
    path('admin/profile/<uuid:uuid>/update-photo/', views.admin_update_profile_photo, name='admin_update_profile_photo'),
    
    # Password Change
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html', success_url='/accounts/password-change/done/'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    
    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html', email_template_name='emails/password_reset_email.html', success_url='/accounts/password-reset/done/'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', success_url='/accounts/reset/done/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
