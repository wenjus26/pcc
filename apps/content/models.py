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

class Resource(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Ressource')
        verbose_name_plural = _('Ressources')

    def __str__(self):
        return self.title
