from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    CITIZEN = 'citizen'
    INSTITUTION = 'institution'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (CITIZEN, _('Citoyen / Membre')),
        (INSTITUTION, _('Institution / Entreprise')),
        (ADMIN, _('Administrateur')),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CITIZEN
    )
    
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = _('Utilisateur')
        verbose_name_plural = _('Utilisateurs')
