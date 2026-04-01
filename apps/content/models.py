from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __str__(self):
        return self.title

class Event(models.Model):
    FORUM = 'forum'
    MASTERCLASS = 'masterclass'
    CONFERENCE = 'conference'
    
    EVENT_TYPES = [
        (FORUM, _('Forum')),
        (MASTERCLASS, _('Masterclass')),
        (CONFERENCE, _('Conférence')),
    ]
    
    import uuid
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default=MASTERCLASS)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Événement')
        verbose_name_plural = _('Événements')

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.title}"

class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField(help_text="Lien YouTube complet")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Vidéo')
        verbose_name_plural = _('Vidéos')

    def __str__(self):
        return self.title

    def get_youtube_id(self):
        # Helper to extract ID from URL
        import re
        regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        match = re.search(regex, self.youtube_url)
        return match.group(1) if match else None

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('file', _('Fichier')),
        ('video', _('Vidéo (URL)')),
        ('link', _('Lien Externe')),
    ]
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default='file')
    file = models.FileField(upload_to='resources/', null=True, blank=True)
    video_url = models.URLField(blank=True, help_text="Lien YouTube ou Vimeo")
    external_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Ressource')
        verbose_name_plural = _('Ressources')

    def __str__(self):
        return f"[{self.get_resource_type_display()}] {self.title}"

class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cours / MOOC')
        verbose_name_plural = _('Cours / MOOCs')

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True)
    content = models.TextField(blank=True)
    resources = models.ManyToManyField(Resource, blank=True)
    
    class Meta:
        verbose_name = _('Leçon')
        verbose_name_plural = _('Leçons')
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class GalleryImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Image Galerie')
        verbose_name_plural = _('Images Galerie')

    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Inscription Événement')
        verbose_name_plural = _('Inscriptions Événements')
        unique_together = ('event', 'email')

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"
