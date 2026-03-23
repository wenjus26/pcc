import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from apps.citizens.models import Category, Skill, CitizenProfile
from apps.institutions.models import InstitutionProfile, Opportunity
from apps.content.models import Post, Event

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the PCC-BP database with initial premium data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # 1. Categories & Skills
        categories_data = {
            'Informatique & Digital': ['Développement Web', 'Data Science', 'Intelligence Artificielle', 'Cybersécurité', 'Cloud Computing'],
            'Génie Civil & Architecture': ['Architecture Durable', 'Urbanisme', 'Gestion de Chantier', 'Eco-Design', 'Calcul de Structure'],
            'Management & Stratégie': ['Gestion de Projet', 'Leadership', 'Business Intelligence', 'Gouvernance Publique', 'Finances'],
            'Santé & Social': ['Santé Publique', 'Biomedical', 'Éducation Spécialisée', 'Action Communautaire'],
            'Agriculture & Environnement': ['Agriculture Durable', 'Agro-Écologie', 'Gestion des Eaux', 'Droit de l\'Environnement'],
        }

        created_skills = []
        for cat_name, skills in categories_data.items():
            cat, _ = Category.objects.get_or_create(name=cat_name)
            for skill_name in skills:
                skill, _ = Skill.objects.get_or_create(category=cat, name=skill_name)
                created_skills.append(skill)

        # 2. Institutions
        institutions_info = [
            ('Ministère de l\'Économie Numérique', 'men@gov.bj', 'Cotonou'),
            ('Agence de Développement du Bénin', 'adb@beninlibere.bj', 'Cotonou'),
            ('BENIN-VERT (ONG)', 'eco@bjvert.org', 'Parakou'),
            ('Banque Mondiale Bénin', 'contact@worldbank.bj', 'Cotonou'),
        ]

        inst_profiles = []
        for i, (name, email, loc) in enumerate(institutions_info):
            username = f'inst_{i}'
            user, created = User.objects.get_or_create(
                username=username, 
                defaults={'email': email, 'role': 'INSTITUTION', 'first_name': name}
            )
            if created:
                user.set_password('pass123')
                user.save()
            
            profile, _ = InstitutionProfile.objects.get_or_create(
                user=user,
                defaults={'name': name, 'contact_email': email, 'location': loc, 'description': f'Description de {name}.'}
            )
            inst_profiles.append(profile)

        # 3. Opportunities
        opp_titles = [
            'Architecte Principal : Rénovation Éco-Citoyenne',
            'Consultant en Stratégie Digitale',
            'Expert en Agriculture Durable',
            'Chef de Projet Ville Durable',
            'Analyste de Données Publiques',
        ]

        for title in opp_titles:
            opp, created = Opportunity.objects.get_or_create(
                title=title,
                institution=random.choice(inst_profiles),
                defaults={
                    'description': f'Nous recherchons un expert passionné pour le projet {title}.',
                    'requirements': 'Plus de 5 ans d\'expérience, Master ou Doctorat, Maitrise des outils sectoriels.',
                    'status': 'open',
                    'deadline': timezone.now().date() + timezone.timedelta(days=30)
                }
            )
            if created:
                opp.skills_required.add(*random.sample(created_skills, 3))

        # 4. Blog Posts
        posts_data = [
            ('Innovation au Bénin : Le numérique au service de tous', 'blog-1'),
            ('Comment optimiser son profil citoyen pour attirer les institutions ?', 'blog-2'),
            ('Les masterclasses de Janvier : Le calendrier est sorti !', 'blog-3'),
        ]

        for title, slug in posts_data:
            Post.objects.get_or_create(
                title=title,
                slug=slug,
                defaults={
                    'content': 'L\'innovation citoyenne est au cœur du développement métropolitain.',
                    'author': User.objects.first(),
                    'is_published': True
                }
            )

        # 5. Events
        events_data = [
            ('Forum de l\'Innovation Durable', 'forum', 'Cotonou'),
            ('Masterclass : Leadership & Stratégie', 'masterclass', 'Abomey-Calavi'),
            ('Conférence Annuelle PCC 2026', 'conference', 'Ouidah'),
        ]

        for title, etype, loc in events_data:
            Event.objects.get_or_create(
                title=title,
                event_type=etype,
                defaults={
                    'date': timezone.now() + timezone.timedelta(days=random.randint(5, 50)),
                    'location': loc,
                    'description': f'Un événement exceptionnel autour de {title}.'
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded PCC-BP database!'))
