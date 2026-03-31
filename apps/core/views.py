import random
from django.shortcuts import render
from django.http import JsonResponse
from apps.citizens.models import CitizenProfile
from apps.institutions.models import Opportunity
from apps.content.models import Post

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Notification, NewsletterSubscriber

def home(request):
    latest_opportunities = Opportunity.objects.filter(status='open').order_by('-created_at')[:3]
    featured_talents = CitizenProfile.objects.filter(is_public=True).order_by('?')[:3]
    # Handle optional Post model if it exists
    context = {
        'latest_opportunities': latest_opportunities,
        'featured_talents': featured_talents,
    }
    return render(request, 'core/home.html', context)

def search(request):
    query = request.GET.get('q', '')
    talents = Opportunity.objects.none()
    opportunities = Opportunity.objects.none()
    
    if query:
        talents = CitizenProfile.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) |
            Q(current_title__icontains=query) |
            Q(bio__icontains=query),
            is_public=True
        )
        opportunities = Opportunity.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query),
            status='open'
        )
        
    return render(request, 'core/search_results.html', {
        'query': query,
        'talents': talents,
        'opportunities': opportunities
    })

@login_required
def notifications(request):
    notifs = request.user.notifications.all()
    # Mark as read when viewing
    notifs.update(is_read=True)
    return render(request, 'core/notifications.html', {'notifications': notifs})

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

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email manquant.'}, status=400)
        
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            # Optionally send a confirmation email
            from .utils import send_pcc_email
            send_pcc_email(
                subject='Inscription Newsletter PCC',
                template_name='emails/newsletter_welcome.html',
                context={'email': email},
                recipient_list=[email],
                request=request,
            )
            return JsonResponse({'status': 'success', 'message': 'Inscription réussie !'})
        else:
            return JsonResponse({'status': 'info', 'message': 'Vous êtes déjà abonné.'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)
