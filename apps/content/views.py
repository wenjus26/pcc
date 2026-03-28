from django.shortcuts import render, get_object_or_404
from .models import Event

def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'content/event_list.html', {'events': events})

def programme_societe(request):
    return render(request, 'content/programme_societe.html')

def gallery(request):
    from .models import GalleryImage
    images = GalleryImage.objects.all().order_by('-created_at')
    return render(request, 'content/gallery.html', {'images': images})

def biography(request):
    return render(request, 'content/biography.html')

def contributions(request):
    if request.method == 'POST':
        # Add suggestion handling logic here if needed
        from django.contrib import messages
        messages.success(request, "Votre suggestion a été reçue. Merci pour votre contribution.")
    return render(request, 'content/contributions.html')
