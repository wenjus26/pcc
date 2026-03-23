from django.shortcuts import render
from apps.citizens.models import CitizenProfile
from apps.institutions.models import Opportunity
from apps.content.models import Post

def home(request):
    latest_opportunities = Opportunity.objects.filter(status='open').order_by('-created_at')[:3]
    featured_talents = CitizenProfile.objects.filter(is_public=True).order_by('?')[:3]
    recent_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    
    context = {
        'latest_opportunities': latest_opportunities,
        'featured_talents': featured_talents,
        'recent_posts': recent_posts,
    }
    return render(request, 'core/home.html', context)

def error_400(request, exception=None):
    return render(request, 'errors/400.html', status=400)

def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)
