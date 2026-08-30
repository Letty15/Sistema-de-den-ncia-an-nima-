from django.contrib import admin
from .models import usuarios

@admin.register(usuarios)
class usuariosAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'rg', 'endereco')
    search_fields = ('user__username', 'cpf', 'rg')
    list_filter = ('endereco',)
# Register your models here.
