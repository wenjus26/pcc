from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.citizens.models import CitizenProfile
from apps.institutions.models import Opportunity

class Application(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (PENDING, _('En attente')),
        (ACCEPTED, _('Acceptée')),
        (REJECTED, _('Refusée')),
    ]
    
    citizen = models.ForeignKey(CitizenProfile, on_delete=models.CASCADE, related_name='applications')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    cover_letter = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Candidature')
        verbose_name_plural = _('Candidatures')
        unique_together = ('citizen', 'opportunity')

    def __str__(self):
        return f"{self.citizen.user.username} -> {self.opportunity.title}"

class Match(models.Model):
    citizen = models.ForeignKey(CitizenProfile, on_delete=models.CASCADE, related_name='matches')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='matches')
    score = models.FloatField(default=0.0) # For matchmaking logic
    
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matchs')
        unique_together = ('citizen', 'opportunity')
