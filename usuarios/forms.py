from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class CadastroUsuarioForm(UserCreationForm):
    cpf = forms.CharField(max_length=14, label='CPF')
    rg = forms.CharField(max_length=20, label='RG')
    endereco = forms.CharField(max_length=255, label='Endereço')

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'cpf', 'rg', 'endereco')


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'cpf', 'rg', 'endereco']