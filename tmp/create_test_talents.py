import os
import django
import sys

# Add current directory to path
sys.path.append(os.getcwd())

# Setup Django 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.citizens.models import CitizenProfile

def create_talent(username, email, first_name, last_name, role, title):
    # Check if user already exists
    user, created = CustomUser.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': role,
            'is_active': True
        }
    )
    
    if created:
        user.set_password('PccTest2026!')
        user.save()
        print(f"✅ Utilisateur {username} créé.")
    else:
        # Update email if changed
        user.email = email
        user.save()
        print(f"ℹ️ Utilisateur {username} mis à jour.")
        
    # Create profile
    profile, p_created = CitizenProfile.objects.get_or_create(
        user=user,
        defaults={
            'current_title': title,
            'is_validated': False,
            'bio': f"Profil de test pour {first_name} {last_name}.",
            'location': 'littoral'
        }
    )
    
    if p_created:
        print(f"✅ Profil citoyen créé pour {username} (en attente de validation).")
    else:
        profile.is_validated = False
        profile.save()
        print(f"ℹ️ Profil citoyen réinitialisé à 'En attente' pour {username}.")

# Execution
create_talent('rejuste_wenou', 'rejustewenoumi@gmail.com', 'Réjuste', 'WENOU', 'expert_ca', 'Expert Conseil Administration')
create_talent('rw_mis_services', 'rw.mis.services@gmail.com', 'RW MIS', 'Services', 'talent', 'Consultant Services MIS')

print("\n🚀 Bravo ! Les deux comptes de test sont prêts dans votre base de données.")
