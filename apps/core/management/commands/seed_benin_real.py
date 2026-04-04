import random
import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.citizens.models import Category, Skill, CitizenProfile, Experience, Education
from apps.institutions.models import InstitutionProfile, Opportunity
from apps.content.models import Post, Event, Resource

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with REALISTIC Beninese data for PCC-Benin with matching skills'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Mise à jour de la base de données avec des compétences ciblées par offre...')

        # 1. Catégories & Compétences adaptées au contexte béninois
        categories_data = {
            'Agriculture & Agro-industrie': [
                'Transformation du Karité', 'Production de Soja Bio', 'Aviculture Moderne', 
                'Agro-business béninois', 'Irrigation Goute-à-Goute', 'Elevage Piscicole'
            ],
            'Économie Numérique & Digital': [
                'E-Gouvernance (X-Road)', 'Développement Python/Django', 'Gestion de Données ANIP', 
                'Cybersécurité Nationale', 'Mobile Money & Fintech', 'Intelligence Artificielle'
            ],
            'Administration & Gouvernance': [
                'Gestion FAP (Fonds d\'Appui à la Production)', 'Droit OHADA', 'Décentralisation & Communes', 
                'Passation des Marchés Publics', 'Audit de Performance', 'Gestion de la Diaspora', 'Audit financier'
            ],
            'Santé & Social': [
                'Santé Communautaire', 'Gestion d\'Assurance Maladie (ARCH)', 'Epidémiologie', 
                'Génie Biomédical', 'Soins Infirmiers Spécialisés'
            ],
            'Infrastructures & Énergie': [
                'Solaire Photovoltaïque', 'Génie Civil-BTP', 'Architecture Durable', 'Urbanisme Durable', 
                'Maintenance Réseaux SBEE', 'Assainissement Pluvial'
            ],
        }

        all_skills = {}
        for cat_name, skills in categories_data.items():
            cat, _ = Category.objects.get_or_create(name=cat_name)
            all_skills[cat_name] = []
            for skill_name in skills:
                skill, _ = Skill.objects.get_or_create(category=cat, name=skill_name)
                all_skills[cat_name].append(skill)

        # 2. Institutions Réelles (Identifiées ou créées)
        institutions_info = [
            ('Présidence de la République du Bénin', 'contact@presidence.bj', 'littoral', 'Palais de la Marina, Cotonou'),
            ('Ministère du Numérique et de la Digitalisation', 'contact@numerique.bj', 'littoral', 'Cotonou'),
            ('Agence de Développement de Sèmè City', 'info@semecity.bj', 'atlantique', 'Ouidah/Cotonou'),
            ('GDIZ - Zone Industrielle de Glo-Djigbé', 'contact@gdizbenin.com', 'atlantique', 'Glo-Djigbé'),
            ('FNDA (Fonds National de Développement Agricole)', 'fnda@agriculture.bj', 'oueme', 'Porto-Novo'),
            ('Ministère de l\'Économie et des Finances', 'mef@finances.bj', 'littoral', 'Cotonou'),
        ]

        inst_profiles = []
        for name, email, dept, loc in institutions_info:
            username = email.split('@')[0]
            user, created = User.objects.get_or_create(
                username=username, 
                defaults={'email': email, 'role': 'institution', 'first_name': name}
            )
            if created:
                user.set_password('Benin2026@')
                user.save()
            
            profile, _ = InstitutionProfile.objects.get_or_create(
                user=user,
                defaults={
                    'name': name, 
                    'contact_email': email, 
                    'location': f"{loc} ({dept.capitalize()})", 
                    'description': f"Institution stratégique de la République du Bénin : {name}."
                }
            )
            inst_profiles.append(profile)

        # 3. Offres / Opportunités Nationales avec COMPÉTENCES ADAPTÉES
        opp_data = [
            {
                'title': 'Consultant Senior : Modernisation de l\'E-Gouvernance',
                'inst': 'MND',
                'desc': 'Piloter la mise en place de X-Road et des services de l\'Etat en ligne.',
                'reqs': '10 ans exp, PhD/Ingénieur, connaissance de l\'écosystème béninois.',
                'skills': ['E-Gouvernance (X-Road)', 'Cybersécurité Nationale', 'Intelligence Artificielle']
            },
            {
                'title': 'Chef de Projet : Extension de la GDIZ',
                'inst': 'GDIZ',
                'desc': 'Coordination technique des travaux de la phase 2 de la zone industrielle.',
                'reqs': 'Ingénieur Civil, 15 ans exp, gestion de chantiers industriels.',
                'skills': ['Génie Civil-BTP', 'Urbanisme Durable', 'Assainissement Pluvial']
            },
            {
                'title': 'Expert en Valorisation des Filières Karité et Ananas',
                'inst': 'FNDA',
                'desc': 'Optimiser les chaînes de valeur de l\'ananas et du karité pour l\'export.',
                'reqs': 'Agro-économiste reconnu, expert en transformation.',
                'skills': ['Transformation du Karité', 'Agro-business béninois', 'Irrigation Goute-à-Goute']
            },
            {
                'title': 'Lead Auditor : Réforme des Finances Publiques',
                'inst': 'MEF',
                'desc': 'Mise en œuvre des réformes de transparence et contrôle budgétaire.',
                'reqs': 'Expert-comptable / Auditeur, connaissance des finances de l\'Etat.',
                'skills': ['Audit de Performance', 'Passation des Marchés Publics', 'Audit financier']
            },
            {
                'title': 'Architecte : Nouveau siège du Parlement à Porto-Novo',
                'inst': 'Présidence',
                'desc': 'Suivi architectural de la construction du bâtiment emblématique à Porto-Novo.',
                'reqs': 'Architecte agréé, expertise bâtiments publics eco-durables.',
                'skills': ['Architecture Durable', 'Urbanisme Durable', 'Génie Civil-BTP']
            },
            {
                'title': 'Spécialiste Mobile Money & Fintech',
                'inst': 'MND',
                'desc': 'Encadrer le développement des paiements numériques locaux.',
                'reqs': 'Expert Fintech, 5 ans exp.',
                'skills': ['Mobile Money & Fintech', 'Cybersécurité Nationale', 'Intelligence Artificielle']
            }
        ]

        for entry in opp_data:
            # Find institution or default
            inst = next((i for i in inst_profiles if entry['inst'].lower() in i.name.lower()), inst_profiles[0])
            
            opp, created = Opportunity.objects.get_or_create(
                title=entry['title'],
                institution=inst,
                defaults={
                    'description': entry['desc'] + " Projet stratégique du PAG 2.",
                    'requirements': entry['reqs'],
                    'status': 'open',
                    'deadline': timezone.now().date() + timezone.timedelta(days=60)
                }
            )
            
            # CLEAR PREVIOUS SKILLS and ADD TARGETED ONES
            opp.skills_required.clear()
            for s_name in entry['skills']:
                skill = Skill.objects.filter(name=s_name).first()
                if skill:
                    opp.skills_required.add(skill)
            
            self.stdout.write(f"  - Offre configurée : {opp.title} with {opp.skills_required.count()} skills.")

        self.stdout.write(self.style.SUCCESS('\n✅ Toutes les offres ont maintenant les compétences adaptées atttribuées !'))
