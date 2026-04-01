from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Opportunity

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
