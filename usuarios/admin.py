from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'cpf', 'rg', 'endereco')
    search_fields = ('username', 'cpf', 'rg')
    list_filter = ('endereco',)
# Register your models here.
