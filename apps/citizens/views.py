import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import CitizenProfile, Skill

def talent_list(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    skill_query = request.GET.get('skill', '')

    queryset = CitizenProfile.objects.filter(is_public=True)

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
    
    # Check if the current user is the owner of the profile
    if profile.user != request.user:
        return redirect('citizens:profile_detail', uuid=uuid)

    if request.method == 'POST':
        # Simple processing for the form without using complex forms.ModelForm first for demonstration, 
        # but in real usage we'd use ModelForm.
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        profile.availability = request.POST.get('availability', profile.availability)
        profile.current_title = request.POST.get('current_title', profile.current_title)
        profile.years_of_experience = int(request.POST.get('years_of_experience', profile.years_of_experience) or 0)
        profile.is_public = request.POST.get('is_public') == 'on'
        profile.save()
        return redirect('citizens:profile_detail', uuid=uuid)

    return render(request, 'citizens/profile_form.html', {'profile': profile})
