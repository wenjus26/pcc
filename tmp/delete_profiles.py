from django.contrib.auth import get_user_model
from apps.citizens.models import CitizenProfile

User = get_user_model()

# Liste des noms à supprimer (partiels ou complets)
profiles_to_delete = [
    {'first': 'Amina', 'last': 'Talebi'},
    {'first': 'Luc', 'last': 'Gnacadja'}
]

print("--- Suppression des profils citoyens spécifiques ---")

for data in profiles_to_delete:
    users = User.objects.filter(first_name__icontains=data['first'], last_name__icontains=data['last'])
    if users.exists():
        for user in users:
            print(f"Suppression de l'utilisateur : {user.first_name} {user.last_name} ({user.username})")
            user.delete()
    else:
        # Essayer par nom complet dans first_name ou last_name si séparés différemment
        alt_users = User.objects.filter(username__icontains=data['first'].lower()) | User.objects.filter(username__icontains=data['last'].lower())
        if alt_users.exists():
            for user in alt_users:
                if data['first'].lower() in user.first_name.lower() or data['last'].lower() in user.last_name.lower():
                    print(f"Suppression possible (match partiel) : {user.first_name} {user.last_name} ({user.username})")
                    user.delete()
        else:
            print(f"Aucun utilisateur trouvé pour : {data['first']} {data['last']}")

print("--- Nettoyage terminé ---")
