from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'phone_number', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Restriction: Seuls les talents locaux et de la diaspora peuvent s'inscrire via ce formulaire
        self.fields['role'].choices = [
            (CustomUser.TALENT, _('Talent & Compétence (Local)')),
            (CustomUser.DIASPORA, _('Talent & Compétence (Diaspora)')),
        ]
        
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition-all'
            })
