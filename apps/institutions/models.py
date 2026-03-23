import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.citizens.models import Skill

class InstitutionProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='institution_profile')
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='institution_logos/', blank=True, null=True)
    description = models.TextField()
    website = models.URLField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Profil Institutionnel')
        verbose_name_plural = _('Profils Institutionnels')

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    DRAFT = 'draft'
    OPEN = 'open'
    CLOSED = 'closed'
    
    STATUS_CHOICES = [
        (DRAFT, _('Brouillon')),
        (OPEN, _('Ouvert')),
        (CLOSED, _('Clôturé')),
    ]
    
    institution = models.ForeignKey(InstitutionProfile, on_delete=models.CASCADE, related_name='opportunities')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    
    skills_required = models.ManyToManyField(Skill, related_name='opportunities')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    deadline = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Opportunité / Projet')
        verbose_name_plural = _('Opportunités / Projets')

    def __str__(self):
        return self.title
