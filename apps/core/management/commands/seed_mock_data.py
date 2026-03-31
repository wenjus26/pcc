from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.citizens.models import CitizenProfile, Category
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed mock citizen profiles for the skill map'

    def handle(self, *args, **options):
        departments = [
            'ALIBORI', 'ATACORA', 'ATLANTIQUE', 'BORGOU', 'COLLINES', 
            'COUFFO', 'DONGA', 'LITTORAL', 'MONO', 'OUEME', 'PLATEAU', 'ZOU'
        ]
        
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('No categories found. Run seed_categories first.'))
            return

        for i in range(50):
            username = f'citizen_{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com'}
            )
            if created:
                user.set_password('password123')
                user.save()
            
            profile, _ = CitizenProfile.objects.get_or_create(user=user)
            profile.location = random.choice(departments)
            profile.current_title = f'Expert in {random.choice(categories).name}'
            profile.is_public = True
            profile.is_validated = True
            profile.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded 50 mock profiles.'))
