from django import forms
from .models import ConteudoEducativo


class ConteudoEducativoForm(forms.ModelForm):
    class Meta:
        model = ConteudoEducativo
        fields = ['titulo', 'categoria', 'corpo', 'canais_apoio']