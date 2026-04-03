from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from apps.citizens.models import CitizenProfile
from apps.institutions.models import InstitutionProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crée automatiquement le profil approprié pour chaque nouvel utilisateur.
    """
    if created:
        if instance.role == CustomUser.ADMIN:
            return  # Pas de profil automatique pour l'admin global
        
        elif instance.role == CustomUser.INSTITUTION:
            # Créer un profil institutionnel vide
            InstitutionProfile.objects.get_or_create(
                user=instance,
                name=instance.username  # Nom par défaut
            )
        
        else:
            # Créer un profil citoyen par défaut pour tous les autres segments (Experts, Soutien, Talents, etc.)
            CitizenProfile.objects.get_or_create(user=instance)

