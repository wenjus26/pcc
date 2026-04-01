from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Opportunity

def opportunity_list(request):
    query = request.GET.get('q', '')
    queryset = Opportunity.objects.filter(status='open')
    
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
    }
    return render(request, 'institutions/opportunity_list.html', context)

def opportunity_detail(request, uuid):
    opportunity = get_object_or_404(Opportunity, uuid=uuid)
    return render(request, 'institutions/opportunity_detail.html', {'opportunity': opportunity})
