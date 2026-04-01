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
        InstitutionProfile.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            website=self.cleaned_data['website']
        )
        return user

class AdminCitizenCreateForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    current_title = forms.CharField(max_length=255, required=False)
    
    def save(self):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            role=CustomUser.CITIZEN
        )
        CitizenProfile.objects.create(
            user=user,
            current_title=self.cleaned_data['current_title'],
            is_validated=True  # Usually admin created is pre-validated
        )
        return user
