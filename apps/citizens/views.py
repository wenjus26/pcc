import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import CitizenProfile, Skill
from .forms import CitizenProfileForm, ExperienceFormSet, EducationFormSet

def skill_map(request):
    """
    Displays the geographic distribution of talents across Benin's departments.
    """
    stats = CitizenProfile.objects.filter(is_validated=True).values('location').annotate(total=Count('location'))
    
    # Map the results to a dictionary for easier access in the template
    location_data = {item['location']: item['total'] for item in stats if item['location']}
    
    import json
    context = {
        'location_data': location_data,
        'location_data_json': json.dumps(location_data),
        'departments': CitizenProfile.DEPARTMENTS,
    }
    return render(request, 'citizens/skill_map.html', context)

def talent_list(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    skill_query = request.GET.get('skill', '')

    queryset = CitizenProfile.objects.filter(is_public=True, is_validated=True)

    if query:
        queryset = queryset.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(current_title__icontains=query) |
            Q(bio__icontains=query)
        )

    if location:
        queryset = queryset.filter(location__icontains=location)

    if skill_query:
        queryset = queryset.filter(skills__name__icontains=skill_query)

    queryset = queryset.distinct().order_by('-created_at')

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'talents': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'citizens/talent_list.html', context)

def profile_detail(request, uuid):
    profile = get_object_or_404(CitizenProfile, uuid=uuid)
    return render(request, 'citizens/profile_detail.html', {'profile': profile})

@login_required
def profile_edit(request, uuid):
    profile = get_object_or_404(CitizenProfile, uuid=uuid)
    
    if profile.user != request.user:
        return redirect('citizens:profile_detail', uuid=uuid)

    # Access restricted to validated profiles only (per user's audio request)
    if not profile.is_validated:
        from django.contrib import messages
        messages.warning(request, "Votre profil doit être validé par un administrateur avant de pouvoir modifier vos informations détaillées.")
        return redirect('citizens:profile_detail', uuid=uuid)

    if request.method == 'POST':
        form = CitizenProfileForm(request.POST, request.FILES, instance=profile)
        experience_formset = ExperienceFormSet(request.POST, request.FILES, instance=profile)
        education_formset = EducationFormSet(request.POST, request.FILES, instance=profile)
        
        if form.is_valid() and experience_formset.is_valid() and education_formset.is_valid():
            # Automatically require re-validation when sensitive info matches
            profile = form.save(commit=False)
            profile.is_validated = False  # Set to unvalidated upon modification for re-verification
            profile.save()
            
            experience_formset.save()
            education_formset.save()
            
            if 'cv_file' in request.FILES:
                from .models import Document
                Document.objects.create(
                    profile=profile,
                    doc_type='cv',
                    title="CV Principal",
                    file=request.FILES['cv_file']
                )

            # Send Email Confirmation
            from apps.core.utils import send_pcc_email
            subject = "Mise à jour de votre profil PCC réussie"
            context = {
                'user': request.user,
                'profile': profile,
            }
            send_pcc_email(subject, 'emails/profile_updated_confirmation.html', context, [request.user.email], request=request)

            from django.contrib import messages
            messages.success(request, "Votre profil a été mis à jour avec succès. Un email de confirmation vous a été envoyé.")
            return redirect('citizens:profile_detail', uuid=uuid)
    else:
        form = CitizenProfileForm(instance=profile)
        experience_formset = ExperienceFormSet(instance=profile)
        education_formset = EducationFormSet(instance=profile)

    context = {
        'profile': profile,
        'form': form,
        'experience_formset': experience_formset,
        'education_formset': education_formset
    }
    return render(request, 'citizens/profile_form.html', context)

@login_required
def talent_register(request):
    """
    Dedicated and autonomous registration page for competencies.
    Allows adding CV, photo, and charter signature.
    """
    profile, created = CitizenProfile.objects.get_or_create(user=request.user)
    
    # Check if already validated
    if profile.is_validated:
        from django.contrib import messages
        messages.info(request, "Votre profil a déjà été validé.")
        return redirect('citizens:profile_detail', uuid=profile.uuid)
        
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.current_title = request.POST.get('current_title', '')
        profile.years_of_experience = int(request.POST.get('years_of_experience', 0) or 0)
        
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
            
        if request.POST.get('charter_signed') == 'on':
            profile.charter_signed = True
            
        # 1-click validation logic: Here we just mark for admin, but the user requested "système permettant la validation en un clic".
        # If they mean admin can validate it in 1-click, we set it False. If they want auto-validate when filled, we'll set it to True.
        # "Le transfert automatique des profils validés vers la base de données des compétences consultables".
        # I'll leave `is_validated` to False, but an admin interface or button from profile can validate it.
        profile.is_validated = False  # Pending review
        profile.save()
        
        if 'cv_file' in request.FILES:
            from .models import Document
            Document.objects.create(
                profile=profile,
                doc_type='cv',
                title="Mon Curriculum Vitae",
                file=request.FILES['cv_file']
            )
            
        from django.contrib import messages
        messages.success(request, "Votre profil a été soumis et est en attente de validation.")
        return redirect('citizens:talent_list')

    return render(request, 'citizens/talent_register.html', {'profile': profile})


from django.http import HttpResponse
from .services import generate_excel_template

@login_required # Ou `staff_member_required` idéalement, selon votre système
def download_template(request):
    """
    Génère et télécharge un modèle Excel vierge pour l'import massif d'utilisateurs.
    """
    if not request.user.is_staff:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("Seuls les administrateurs peuvent télécharger ce modèle.")
        
    wb = generate_excel_template()
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="PCC_Import_Template.xlsx"'
    
    wb.save(response)
    return response

from .services import process_excel_import

@login_required
def import_data(request):
    """
    Gère l'upload du fichier Excel d'import et renvoie le rapport Word.
    """
    if not request.user.is_staff:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("Seuls les administrateurs peuvent importer des données.")
        
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Validation d'extension
        if not excel_file.name.endswith('.xlsx'):
            from django.contrib import messages
            messages.error(request, "Veuillez uploader un fichier Excel (.xlsx) valide.")
            # Normalement on redirige vers le dashboard
            return redirect('accounts:admin_dashboard')
            
        # Traitement et récupération du rapport Word
        try:
            from django.utils import timezone
            report_io = process_excel_import(excel_file)
            
            # Envoi en tant que téléchargement
            response = HttpResponse(
                report_io.read(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            admin_username = request.user.username
            filename = f"Rapport_Import_{admin_username}_{timestamp}.docx"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Une erreur s'est produite: {str(e)}")
            return redirect('accounts:admin_dashboard')
            
    # Si GET ou erreur, rediriger
    return redirect('accounts:admin_dashboard')
