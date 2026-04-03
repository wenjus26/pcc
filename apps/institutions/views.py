from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Opportunity, InstitutionProfile
from .forms import OpportunityForm

def opportunity_list(request):
    query = request.GET.get('q', '')
    selected_status = request.GET.getlist('status')
    
    # Base queryset
    queryset = Opportunity.objects.all()
    
    # Filter by status if selected, otherwise show 'open' by default
    if selected_status and any(selected_status):
        queryset = queryset.filter(status__in=selected_status)
    else:
        # If no filter selected at all, we show ONLY 'open' (Ouvert)
        # However, if this is a first visit, selected_status will be empty
        queryset = queryset.filter(status='open')
        selected_status = ['open']
    
    if query:
        from django.db.models import Q
        queryset = queryset.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(institution__name__icontains=query)
        )
        
    queryset = queryset.order_by('-created_at')
    
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'opportunities': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'selected_status': selected_status,
    }
    return render(request, 'institutions/opportunity_list.html', context)

def opportunity_detail(request, uuid):
    opportunity = get_object_or_404(Opportunity, uuid=uuid)
    return render(request, 'institutions/opportunity_detail.html', {'opportunity': opportunity})

@login_required
def opportunity_create(request):
    if request.user.role != 'institution':
        messages.error(request, "Seul un compte institutionnel peut publier des appels.")
        return redirect('accounts:dashboard')
    
    profile = get_object_or_404(InstitutionProfile, user=request.user)
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.institution = profile
            opportunity.save()
            form.save_m2m() # Important for skills (ManyToMany)
            messages.success(request, "L'appel à projets a été publié avec succès.")
            return redirect('accounts:dashboard')
    else:
        form = OpportunityForm()
    
    return render(request, 'institutions/opportunity_form.html', {
        'form': form,
        'title': "Publier une Opportunité"
    })

@login_required
def opportunity_edit(request, uuid):
    opportunity = get_object_or_404(Opportunity, uuid=uuid)
    
    # Security: check if institution owns the opportunity
    if opportunity.institution.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cet appel.")
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            messages.success(request, "L'appel à projets a été mis à jour.")
            return redirect('accounts:dashboard')
    else:
        form = OpportunityForm(instance=opportunity)
    
    return render(request, 'institutions/opportunity_form.html', {
        'form': form,
        'title': "Modifier l'Appel",
        'opportunity': opportunity
    })
