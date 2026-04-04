from django.contrib.auth import get_user_model
from apps.institutions.models import InstitutionProfile
from apps.citizens.models import CitizenProfile

User = get_user_model()

emails_to_delete = [
    'ruthadjadji03@gmail.com',
    'rejustewenoumi@gmail.com',
    'cifb@cifb.bj',
    'contact@worldbank.bj',
    'eco@bjvert.org',
    'adb@beninlibere.bj',
    'men@gov.bj'
]

print(f"--- Démarrage de la suppression de {len(emails_to_delete)} entrées spécifiques ---")

users_deleted = 0
for email in emails_to_delete:
    users = User.objects.filter(email__icontains=email)
    count = users.count()
    if count > 0:
        for user in users:
            print(f"Suppression de l'utilisateur : {user.username} ({user.email})")
            user.delete()
            users_deleted += 1
    else:
        print(f"Aucun utilisateur trouvé avec l'email : {email}")

# Nettoyage supplémentaire par nom d'institution au cas où l'email différe légèrement
inst_names = [
    "SODEDECO", "SODECO", "Conseil des Investisseurs Français au Bénin", 
    "Banque Mondiale Bénin", "BENIN-VERT (ONG)", "Agence de Développement du Bénin",
    "Ministère de l'Économie Numérique"
]

inst_deleted = 0
for name in inst_names:
    insts = InstitutionProfile.objects.filter(name__icontains=name)
    for inst in insts:
        user = inst.user
        print(f"Suppression de l'institution : {inst.name} (User: {user.username})")
        user.delete() # Entraîne la suppression du profil via CASCADE
        inst_deleted += 1

print(f"--- Fin de l'opération : {users_deleted} utilisateurs et {inst_deleted} institutions nettoyés ---")
