from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.institutions.models import Opportunity
from apps.matching.models import Application

@login_required
def apply_to_opportunity(request, uuid):
    opportunity = get_object_or_404(Opportunity, uuid=uuid)
    from apps.accounts.models import CustomUser
    from apps.core.models import Notification
    
    # Check if user is an applicant (non-admin, non-institution)
    if request.user.role in [CustomUser.ADMIN, CustomUser.INSTITUTION]:
        messages.error(request, "Seuls les experts et citoyens peuvent postuler aux projets.")
        return redirect('institutions:opportunity_detail', uuid=uuid)
    
    try:
        citizen_profile = request.user.citizen_profile
    except Exception:
        messages.error(request, "Veuillez d'abord compléter votre profil dans votre espace pour postuler.")
        return redirect('accounts:dashboard')
    
    # Check if already applied
    if Application.objects.filter(citizen=citizen_profile, opportunity=opportunity).exists():
        messages.warning(request, "Vous avez déjà postulé à ce projet.")
    else:
        Application.objects.create(
            citizen=citizen_profile,
            opportunity=opportunity,
            status='pending'
        )

        # 1. In-app notification for the applicant
        Notification.objects.create(
            user=request.user,
            title="Candidature Envoyée",
            message=f"Votre candidature pour le projet '{opportunity.title}' a été transmise avec succès.",
            link=f"/institutions/opportunities/{opportunity.uuid}/"
        )
        
        # 2. In-app notification for the institution
        Notification.objects.create(
            user=opportunity.institution.user,
            title="Nouvelle Candidature",
            message=f"L'expert {request.user.get_full_name()} a postulé à votre appel '{opportunity.title}'.",
            link="/accounts/dashboard/"
        )

        # 3. Email confirmation for the applicant
        from apps.core.utils import send_pcc_email
        send_pcc_email(
            subject=f"Confirmation de candidature : {opportunity.title}",
            template_name='emails/application_confirmation.html',
            context={
                'user': request.user,
                'opportunity': opportunity
            },
            recipient_list=[request.user.email],
            request=request,
        )

        messages.success(request, f"Votre candidature pour '{opportunity.title}' a été envoyée avec succès !")
    
    return redirect('accounts:dashboard')
