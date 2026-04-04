from django.contrib.auth import get_user_model

User = get_user_model()

print("--- Nettoyage final des profils de test ---")

# 1. Supprimer les profils spécifiques demandés
specific_names = [
    {'first': 'Amina', 'last': 'Talebi'},
    {'first': 'Luc', 'last': 'Gnacadja'}
]

for data in specific_names:
    users = User.objects.filter(first_name__icontains=data['first'], last_name__icontains=data['last'])
    for user in users:
        print(f"Suppression spécifique (Amina/Luc) : {user.username}")
        user.delete()

# 2. Supprimer TOUS les utilisateurs ayant un username commençant par 'citizen_' ou 'inst_' (anciens tests)
test_patterns = ['citizen_', 'inst_']
for pattern in test_patterns:
    test_users = User.objects.filter(username__startswith=pattern)
    count = test_users.count()
    if count > 0:
        print(f"Suppression de {count} utilisateurs de test (pattern: '{pattern}')...")
        test_users.delete()

print("--- Base de données maintenant épurée des mock data ---")
