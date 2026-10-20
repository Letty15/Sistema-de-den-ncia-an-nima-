from django import forms
from .models import RespostaDenuncia


class RespostaForm(forms.ModelForm):
    class Meta:
        model = RespostaDenuncia
        fields = ['mensagem']   # denuncia e autor são preenchidos na view