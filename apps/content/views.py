from django.shortcuts import render, get_object_or_404
from .models import Event, Course, Lesson

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

def contributions(request):
    if request.method == 'POST':
        # Add suggestion handling logic here if needed
        from django.contrib import messages
        messages.success(request, "Votre suggestion a été reçue. Merci pour votre contribution.")
    return render(request, 'content/contributions.html')
