from django import forms
from .models import Denuncia


class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['tipo_violencia', 'descricao']


class StatusDenunciaForm(forms.ModelForm):
    """Usado pela CAE para atualizar o andamento da denúncia."""

    class Meta:
        model = Denuncia
        fields = ['status']
        labels = {'status': 'Novo status'}