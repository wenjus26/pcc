from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from apps.citizens.models import CitizenProfile
from apps.institutions.models import InstitutionProfile
from apps.matching.models import Match, Application

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send welcome email
            from apps.core.utils import send_pcc_email
            send_pcc_email(
                subject='Bienvenue sur PCC !',
                template_name='emails/welcome.html',
                context={'user': user},
                recipient_list=[user.email],
                request=request,
            )
            
            login(request, user)
            messages.success(request, 'Inscription réussie ! Bienvenue sur PCC.')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    
    if user.role == 'admin':
        return redirect('accounts:admin_dashboard')
    
    # All other segments currently use the citizen/expert dashboard
    if user.role in ['soutien', 'expert_ca', 'expert_hca', 'talent', 'diaspora']:
        try:
            profile = user.citizen_profile
            context = {'user': user, 'profile': profile}
            context['applications'] = profile.applications.all().order_by('-created_at')[:5]
            context['matches'] = Match.objects.filter(citizen=profile).order_by('-score')[:5]
            return render(request, 'accounts/dashboard_citizen.html', context)
        except CitizenProfile.DoesNotExist:
            messages.warning(request, "Veuillez compléter votre profil pour accéder à votre espace.")
            return redirect('core:home')
    
    return redirect('core:home')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('accounts:dashboard')
        
    pending_profiles = CitizenProfile.objects.filter(is_validated=False).order_by('-created_at')
    
    # KPIs calculations
    from .models import CustomUser
    from apps.institutions.models import InstitutionProfile, Opportunity
    from apps.content.models import Event, Video
    
    stats = {
        'total_users': CustomUser.objects.count(),
        'total_citizens': CitizenProfile.objects.count(),
        'total_opportunities': Opportunity.objects.count(),
        'total_events': Event.objects.count(),
        'total_videos': Video.objects.count(),
        'pending_count': pending_profiles.count(),
        'validated_profiles': CitizenProfile.objects.filter(is_validated=True).count(),
        
        # Breakdown by segments
        'soutien': CustomUser.objects.filter(role='soutien').count(),
        'expert_ca': CustomUser.objects.filter(role='expert_ca').count(),
        'expert_hca': CustomUser.objects.filter(role='expert_hca').count(),
        'talent': CustomUser.objects.filter(role='talent').count(),
        'diaspora': CustomUser.objects.filter(role='diaspora').count(),
    }
    
    # Growth (dummy for now or real if data available)
    stats['active_rate'] = round((stats['validated_profiles'] / stats['total_citizens'] * 100), 1) if stats['total_citizens'] > 0 else 0
    
    context = {
        'pending_profiles': pending_profiles,
        'stats': stats,
    }
    return render(request, 'accounts/dashboard_admin.html', context)

@login_required
def admin_profile_detail(request, uuid):
    if request.user.role != 'admin':
        return redirect('accounts:dashboard')
        
    profile = get_object_or_404(CitizenProfile, uuid=uuid)
    return render(request, 'accounts/admin_profile_detail.html', {'profile': profile})

@login_required
def validate_profile(request, uuid):
    if request.user.role != 'admin':
        return redirect('accounts:dashboard')
        
    profile = get_object_or_404(CitizenProfile, uuid=uuid)
    profile.is_validated = True
    profile.save()
    
    # Send email notification after validation
    from apps.core.utils import send_pcc_email
    subject = "Profil Validé - Plateforme Citoyenne des Compétences"
    context = {
        'user': profile.user,
        'profile': profile,
    }
    
    email_sent = send_pcc_email(subject, 'emails/profile_validated.html', context, [profile.user.email], request=request)
    
    if email_sent:
        messages.success(request, f"Le profil de {profile.user.get_full_name()} a été validé avec succès. Un email de confirmation a été envoyé.")
    else:
        messages.warning(request, f"Le profil de {profile.user.get_full_name()} a été validé, mais l'envoi de l'email de notification a échoué. Veuillez vérifier votre configuration SMTP.")
        
    return redirect('accounts:admin_dashboard')

@login_required
def admin_create_event(request):
    if request.user.role != 'admin':
        return redirect('accounts:dashboard')
    
    from .admin_forms import AdminEventForm
    if request.method == 'POST':
        form = AdminEventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "L'événement a été créé avec succès.")
            return redirect('accounts:admin_dashboard')
    else:
        form = AdminEventForm()
    
    return render(request, 'accounts/admin_create_form.html', {
        'form': form,
        'title': "Créer un Événement",
        'icon': 'fa-calendar-plus'
    })

@login_required
def admin_create_institution(request):
    if request.user.role != 'admin':
        return redirect('accounts:dashboard')
    
    from .admin_forms import AdminInstitutionCreateForm
    if request.method == 'POST':
        form = AdminInstitutionCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le compte Institution a été créé avec succès.")
            return redirect('accounts:admin_dashboard')
    else:
        form = AdminInstitutionCreateForm()
    
    return render(request, 'accounts/admin_create_form.html', {
        'form': form,
        'title': "Créer une Institution",
        'icon': 'fa-building'
    })

@login_required
def admin_create_citizen(request):
    if request.user.role != 'admin':
        return redirect('accounts:dashboard')
    
    from .admin_forms import AdminCitizenCreateForm
    if request.method == 'POST':
        form = AdminCitizenCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le compte Talent/Citoyen a été créé avec succès.")
            return redirect('accounts:admin_dashboard')
    else:
        form = AdminCitizenCreateForm()
    
    return render(request, 'accounts/admin_create_form.html', {
        'form': form,
        'title': "Créer un Talent (Citoyen)",
        'icon': 'fa-user-plus'
    })

@login_required
def admin_update_profile_photo(request, uuid):
    if request.user.role != 'admin':
        return redirect('accounts:dashboard')
    
    from apps.citizens.models import CitizenProfile
    profile = get_object_or_404(CitizenProfile, uuid=uuid)
    
    if request.method == 'POST' and request.FILES.get('photo'):
        profile.photo = request.FILES['photo']
        profile.save()
        messages.success(request, f"La photo de {profile.user.get_full_name()} a été mise à jour.")
        
    return redirect('accounts:admin_profile_detail', uuid=uuid)
