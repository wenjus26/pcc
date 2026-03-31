from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Event, Course, Lesson, EventRegistration
from apps.core.utils import send_pcc_email

def course_list(request):
    courses = Course.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'content/course_list.html', {'courses': courses})

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.all()
    
    # Simple logic for current lesson
    lesson_id = request.GET.get('lesson')
    if lesson_id:
        current_lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    else:
        current_lesson = lessons.first()
        
    return render(request, 'content/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'current_lesson': current_lesson
    })

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

def event_detail(request, uuid):
    event = get_object_or_404(Event, uuid=uuid, is_active=True)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        if full_name and email and phone:
            # Check if already registered
            if EventRegistration.objects.filter(event=event, email=email).exists():
                messages.info(request, "Vous êtes déjà inscrit à cet événement.")
            else:
                registration = EventRegistration.objects.create(
                    event=event,
                    full_name=full_name,
                    email=email,
                    phone=phone
                )
                
                # Send confirmation email
                subject = f"Confirmation d'inscription : {event.title}"
                context = {
                    'full_name': full_name,
                    'event': event,
                    'registration': registration,
                }
                send_pcc_email(subject, 'emails/event_registration_confirmation.html', context, [email], request=request)
                
                messages.success(request, f"Félicitations {full_name}, votre inscription à '{event.title}' a été enregistrée ! Un email de confirmation vous a été envoyé.")
        else:
            messages.error(request, "Veuillez remplir tous les champs du formulaire.")
            
    return render(request, 'content/event_detail.html', {'event': event})

def contributions(request):
    if request.method == 'POST':
        # Add suggestion handling logic here if needed
        from django.contrib import messages
        messages.success(request, "Votre suggestion a été reçue. Merci pour votre contribution.")
    return render(request, 'content/contributions.html')
