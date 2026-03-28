import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon name (e.g., fa-code)")

    class Meta:
        verbose_name = _('Catégorie')
        verbose_name_plural = _('Catégories')

    def __str__(self):
        return self.name

class Skill(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = _('Compétence')
        verbose_name_plural = _('Compétences')
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class CitizenProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citizen_profile')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    availability = models.CharField(max_length=100, blank=True)
    is_public = models.BooleanField(default=True)
    
    skills = models.ManyToManyField(Skill, related_name='citizens', blank=True)
    
    # Career summary
    # Career summary
    current_title = models.CharField(max_length=255, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    # Validation & Charter
    photo = models.ImageField(upload_to='citizen_photos/', null=True, blank=True)
    charter_signed = models.BooleanField(default=False, verbose_name=_("Charte d'éthique signée"))
    is_validated = models.BooleanField(default=False, verbose_name=_("Profil Validé"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profil Citoyen')
        verbose_name_plural = _('Profils Citoyens')

    def __str__(self):
        return f"Profile - {self.user.username}"

class Experience(models.Model):
    profile = models.ForeignKey(CitizenProfile, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Expérience')
        verbose_name_plural = _('Expériences')

    def __str__(self):
        return f"{self.position} @ {self.company}"

class Education(models.Model):
    profile = models.ForeignKey(CitizenProfile, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Éducation')
        verbose_name_plural = _('Éducations')

    def __str__(self):
        return f"{self.degree} from {self.institution}"

class Document(models.Model):
    CV = 'cv'
    DIPLOMA = 'diploma'
    CERTIFICATE = 'certificate'
    OTHER = 'other'
    
    DOCUMENT_TYPES = [
        (CV, _('Curriculum Vitae')),
        (DIPLOMA, _('Diplôme')),
        (CERTIFICATE, _('Certificat')),
        (OTHER, _('Autre')),
    ]
    
    profile = models.ForeignKey(CitizenProfile, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default=CV)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='citizen_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def __str__(self):
        return f"{self.get_doc_type_display()}: {self.title}"
