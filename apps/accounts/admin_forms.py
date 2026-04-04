from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from apps.citizens.models import CitizenProfile
from apps.institutions.models import InstitutionProfile
from apps.content.models import Event

class AdminEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'image', 'is_active']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class AdminInstitutionCreateForm(forms.Form):
    username = forms.CharField(max_length=150, label=_("Nom d'utilisateur"))
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Mot de passe"))
    
    name = forms.CharField(max_length=255, label=_("Nom de l'Institution"))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    website = forms.URLField(required=False)
    
    def save(self):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            role=CustomUser.INSTITUTION
        )
        # Récupérer le profil créé par le signal et le mettre à jour
        profile, created = InstitutionProfile.objects.get_or_create(user=user)
        profile.name = self.cleaned_data['name']
        profile.description = self.cleaned_data['description']
        profile.website = self.cleaned_data['website']
        profile.save()
        return user

class AdminCitizenCreateForm(forms.Form):
    username = forms.CharField(max_length=150, label=_("Nom d'utilisateur"))
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Mot de passe"))
    
    first_name = forms.CharField(max_length=150, label=_("Prénom"))
    last_name = forms.CharField(max_length=150, label=_("Nom"))
    current_title = forms.CharField(max_length=255, required=False, label=_("Titre actuel"))
    
    segment = forms.ChoiceField(
        choices=CustomUser.SEGMENT_CHOICES[:-1], # Exclure 'admin'
        label=_("Segmentation / Rôle")
    )

    def save(self):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            role=self.cleaned_data['segment']
        )
        # Récupérer le profil créé par le signal et le mettre à jour
        profile, created = CitizenProfile.objects.get_or_create(user=user)
        profile.current_title = self.cleaned_data['current_title']
        profile.is_validated = True
        profile.save()
        return user

class BroadcastEmailForm(forms.Form):
    target_role = forms.ChoiceField(
        choices=[('all', _('Tous les Utilisateurs'))] + CustomUser.SEGMENT_CHOICES,
        label=_("Destinataires (Segment)")
    )
    subject = forms.CharField(max_length=200, label=_("Sujet de l'Email"))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 10}), label=_("Message à diffuser"))
