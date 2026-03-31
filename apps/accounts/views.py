from django.shortcuts import render, redirect
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
    context = {'user': user}
    
    if user.role == 'citizen':
        try:
            profile = user.citizen_profile
            context['profile'] = profile
            context['applications'] = profile.applications.all().order_by('-created_at')[:5]
            context['matches'] = Match.objects.filter(citizen=profile).order_by('-score')[:5]
        except CitizenProfile.DoesNotExist:
            messages.warning(request, "Veuillez compléter votre profil citoyen.")
            return redirect('core:home')
        return render(request, 'accounts/dashboard_citizen.html', context)
    
    elif user.role == 'institution':
        try:
            profile = user.institution_profile
            context['profile'] = profile
            context['opportunities'] = profile.opportunities.all().order_by('-created_at')
            context['received_applications'] = Application.objects.filter(opportunity__institution=profile).order_by('-created_at')[:10]
        except InstitutionProfile.DoesNotExist:
            messages.warning(request, "Veuillez compléter votre profil institutionnel.")
            return redirect('core:home')
        return render(request, 'accounts/dashboard_institution.html', context)
    
    return redirect('core:home')
