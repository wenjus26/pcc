from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Segments
    SOUTIEN = 'soutien'
    EXPERT_CA = 'expert_ca'
    EXPERT_HCA = 'expert_hca'
    TALENT = 'talent'
    DIASPORA = 'diaspora'
    ADMIN = 'admin'
    
    SEGMENT_CHOICES = [
        (SOUTIEN, _('Soutien Participatif (Ministres/Hauts Cadres)')),
        (EXPERT_CA, _('Expert - Conseil d’Administration PCC')),
        (EXPERT_HCA, _('Expert - Hors Conseil d’Administration PCC')),
        (TALENT, _('Talent & Compétence (Local)')),
        (DIASPORA, _('Talent & Compétence (Diaspora)')),
        (ADMIN, _('Administrateur Système')),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=SEGMENT_CHOICES,
        default=TALENT,
        verbose_name=_("Segmentation")
    )
    
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = _('Utilisateur')
        verbose_name_plural = _('Utilisateurs')
