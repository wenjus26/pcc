from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.institutions.models import Opportunity
from apps.matching.models import Application

@login_required
def apply_to_opportunity(request, uuid):
    opportunity = get_object_or_404(Opportunity, uuid=uuid)
    
    if request.user.role != 'citizen':
        messages.error(request, "Seuls les citoyens peuvent postuler aux projets.")
        return redirect('institutions:opportunity_detail', uuid=uuid)
    
    try:
        citizen_profile = request.user.citizen_profile
    except Exception:
        messages.error(request, "Vous devez avoir un profil citoyen complet pour postuler.")
        return redirect('citizens:talent_register')
    
    # Check if already applied
    if Application.objects.filter(citizen=citizen_profile, opportunity=opportunity).exists():
        messages.warning(request, "Vous avez déjà postulé à ce projet.")
    else:
        Application.objects.create(
            citizen=citizen_profile,
            opportunity=opportunity,
            status='pending'
        )

        # Send application confirmation email
        from apps.core.utils import send_pcc_email
        send_pcc_email(
            subject=f"Confirmation de candidature : {opportunity.title}",
            template_name='emails/application_confirmation.html',
            context={
                'user': request.user,
                'opportunity': opportunity
            },
            recipient_list=[request.user.email],
        )

        messages.success(request, f"Votre candidature pour '{opportunity.title}' a été envoyée avec succès !")
    
    return redirect('accounts:dashboard')
