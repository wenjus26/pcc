from django import forms
from django.forms import inlineformset_factory
from .models import CitizenProfile, Experience, Education

class CitizenProfileForm(forms.ModelForm):
    class Meta:
        model = CitizenProfile
        fields = ['bio', 'current_title', 'location', 'years_of_experience', 'availability', 'is_public']

ExperienceFormSet = inlineformset_factory(
    CitizenProfile, Experience,
    fields=['company', 'position', 'start_date', 'end_date', 'is_current', 'description'],
    extra=1,
    can_delete=True
)

EducationFormSet = inlineformset_factory(
    CitizenProfile, Education,
    fields=['institution', 'degree', 'field_of_study', 'start_date', 'end_date'],
    extra=1,
    can_delete=True
)
