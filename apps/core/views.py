import random
from django.shortcuts import render
from django.http import JsonResponse
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

def talent_locations(request):
    talents = CitizenProfile.objects.filter(is_public=True).exclude(location__isnull=True)
    locations = []
    
    # Mock geocoding mapping for major Benin cities
    geo_map = {
        'Cotonou': [6.3654, 2.4183],
        'Porto-Novo': [6.4969, 2.6289],
        'Abomey-Calavi': [6.4481, 2.3557],
        'Parakou': [9.3372, 2.6303],
        'Ouidah': [6.3667, 2.0833],
    }
    
    for talent in talents:
        # Get coordinates or use a random spread around Cotonou if city not found
        city_coords = geo_map.get(talent.location, [6.3654, 2.4183])
        locations.append({
            'name': talent.user.get_full_name() or talent.user.username,
            'title': talent.current_title or "Expert",
            'lat': city_coords[0] + (random.uniform(-0.05, 0.05)), # Spread markers
            'lng': city_coords[1] + (random.uniform(-0.05, 0.05)),
        })
    return JsonResponse(locations, safe=False)

def error_400(request, exception=None):
    return render(request, 'errors/400.html', status=400)

def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)
