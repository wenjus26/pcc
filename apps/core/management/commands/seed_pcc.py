import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from apps.citizens.models import Category, Skill, CitizenProfile, Experience, Education
from apps.institutions.models import InstitutionProfile, Opportunity
from apps.content.models import Post, Event, Resource, GalleryImage
from apps.matching.models import Application, Match

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the PCC-BP database with comprehensive and premium data'

    def handle(self, *args, **options):
        self.stdout.write('Starting seeding PCC database...')

        # 1. Categories & Skills
        categories_data = {
            'Informatique & Digital': ['Développement Web', 'Data Science', 'Intelligence Artificielle', 'Cybersécurité', 'Cloud Computing', 'UX/UI Design'],
            'Génie Civil & Architecture': ['Architecture Durable', 'Urbanisme', 'Gestion de Chantier', 'Eco-Design', 'Calcul de Structure', 'Expertise Immobilière'],
            'Management & Stratégie': ['Gestion de Projet', 'Leadership', 'Business Intelligence', 'Gouvernance Publique', 'Finances', 'Audit & Conseil'],
            'Santé & Social': ['Santé Publique', 'Biomedical', 'Éducation Spécialisée', 'Action Communautaire', 'Gestion Hospitalière'],
            'Agriculture & Environnement': ['Agriculture Durable', 'Agro-Écologie', 'Gestion des Eaux', 'Droit de l\'Environnement', 'Énergies Renouvelables'],
        }

        created_skills = []
        for cat_name, skills in categories_data.items():
            cat, _ = Category.objects.get_or_create(name=cat_name)
            for skill_name in skills:
                skill, _ = Skill.objects.get_or_create(category=cat, name=skill_name)
                created_skills.append(skill)

        # 2. Institutions
        institutions_info = [
            ('Ministère du Numérique', 'men@gov.bj', 'Cotonou'),
            ('Agence de Développement du Bénin', 'adb@beninlibere.bj', 'Cotonou'),
            ('Sèmè-City', 'contact@semecity.bj', 'Ouidah'),
            ('BENIN-VERT (ONG)', 'eco@bjvert.org', 'Parakou'),
            ('Conseil des Investisseurs Français au Bénin', 'cifb@cifb.bj', 'Cotonou'),
        ]

        inst_profiles = []
        for i, (name, email, loc) in enumerate(institutions_info):
            username = f'inst_{i}'
            user, created = User.objects.get_or_create(
                username=username, 
                defaults={'email': email, 'role': User.INSTITUTION, 'first_name': name}
            )
            if created:
                user.set_password('pass123')
                user.save()
            
            profile, _ = InstitutionProfile.objects.get_or_create(
                user=user,
                defaults={
                    'name': name, 
                    'contact_email': email, 
                    'location': loc, 
                    'description': f'Description institutionnelle de {name}. Contribuant au développement national.'
                }
            )
            inst_profiles.append(profile)

        # 3. Citizens
        citizen_names = [
            ('Marc', 'Agbogbo'), ('Sophie', 'Sossou'), ('Jean', 'Koffi'), 
            ('Amina', 'Talebi'), ('Serge', 'Houngbo'), ('Bernadette', 'Alapini')
        ]

        citizen_profiles = []
        for first, last in citizen_names:
            username = f"{first.lower()}.{last.lower()}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f"{username}@mail.bj", 'role': User.CITIZEN, 'first_name': first, 'last_name': last}
            )
            if created:
                user.set_password('pass123')
                user.save()

            profile, _ = CitizenProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'Expert passionné par {random.choice(created_skills).name}. Plus de 5 ans d’expérience.',
                    'location': random.choice(['Cotonou', 'Porto-Novo', 'Abomey-Calavi']),
                    'current_title': 'Consultant Senior',
                    'years_of_experience': random.randint(2, 15),
                    'is_validated': True,
                    'is_public': True
                }
            )
            profile.skills.add(*random.sample(created_skills, 4))
            citizen_profiles.append(profile)

            # Experience & Education
            Experience.objects.get_or_create(
                profile=profile,
                company="Cabinet International",
                position="Consultant",
                start_date=timezone.now().date() - timezone.timedelta(days=1000),
                defaults={'description': 'Gestion de projets complexes.'}
            )
            Education.objects.get_or_create(
                profile=profile,
                institution="Université d'Abomey-Calavi",
                degree="Master Professionnel",
                field_of_study="Gestion / Ingénierie",
                start_date=timezone.now().date() - timezone.timedelta(days=2000)
            )

        # 4. Opportunities
        opp_titles = [
            'Architecte Principal : Rénovation Éco-Citoyenne',
            'Consultant en Stratégie Digitale National',
            'Expert en Agriculture de Précision',
            'Chef de Projet Urbanisme Durable',
            'Lead Data Scientist pour le Secteur Public',
            'Expert Mobilité Électrique',
        ]

        opportunities = []
        for title in opp_titles:
            opp, created = Opportunity.objects.get_or_create(
                title=title,
                institution=random.choice(inst_profiles),
                defaults={
                    'description': f'Nous recherchons un leader technique pour piloter le projet {title}. Une initiative clé pour l’écosystème béninois.',
                    'requirements': 'Expert reconnu, capable de travailler dans un environnement dynamique. Master/Ingénieur minimum.',
                    'status': 'open',
                    'deadline': timezone.now().date() + timezone.timedelta(days=random.randint(20, 60))
                }
            )
            if created:
                opp.skills_required.add(*random.sample(created_skills, 3))
            opportunities.append(opp)

        # 5. Matching & Applications
        for profile in citizen_profiles:
            for _ in range(2):
                opp = random.choice(opportunities)
                Application.objects.get_or_create(
                    citizen=profile,
                    opportunity=opp,
                    defaults={'cover_letter': "Passionné par ce projet, je souhaite apporter mon expertise."}
                )
                Match.objects.get_or_create(
                    citizen=profile,
                    opportunity=opp,
                    defaults={'score': random.uniform(70, 95)}
                )

        # 6. Content (Blog, Events, Resources)
        Post.objects.get_or_create(
            title='Innovation 2026 : Le Bénin s’affirme',
            slug='innovation-2026',
            defaults={
                'content': 'L’accélération digitale au Bénin est un exemple régional.',
                'author': User.objects.first(),
                'is_published': True
            }
        )

        Event.objects.get_or_create(
            title='Sommet des Compétences Citoyennes',
            date=timezone.now() + timezone.timedelta(days=30),
            defaults={'event_type': 'conference', 'location': 'Palais des Congrès, Cotonou', 'description': 'Réunion annuelle.'}
        )

        Resource.objects.get_or_create(
            title='Guide de l’Expert Citoyen',
            defaults={'description': 'Documentation complète sur la plateforme.'}
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(citizen_profiles)} profiles, {len(opportunities)} projects and all related models!'))
