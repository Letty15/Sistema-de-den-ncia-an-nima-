from django import forms
from .models import ConteudoEducativo, CanalApoio


class ConteudoEducativoForm(forms.ModelForm):
    # O autor não é escolhido: a view grava o membro da CAE que está logado.
    class Meta:
        model = ConteudoEducativo
        fields = ['titulo', 'categoria', 'corpo', 'canais_apoio']


class CanalApoioForm(forms.ModelForm):
    class Meta:
        model = CanalApoio
        fields = ['nome', 'descricao', 'contato']