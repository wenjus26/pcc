from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Opportunity
from apps.citizens.models import Skill

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'description', 'requirements', 'skills_required', 'status', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition-all',
                'placeholder': _("Ex: Expert en Cybersécurité pour le Gouvernement")
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition-all',
                'rows': 4,
                'placeholder': _("Décrivez le projet et ses objectifs...")
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'w-full px-5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition-all',
                'rows': 4,
                'placeholder': _("Listez les qualifications requises...")
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'w-full px-5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition-all',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition-all'
            }),
            'skills_required': forms.SelectMultiple(attrs={
                'class': 'w-full px-5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition-all',
            })
        }
