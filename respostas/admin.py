from django.contrib import admin
from .models import RespostaDenuncia


@admin.register(RespostaDenuncia)
class RespostaDenunciaAdmin(admin.ModelAdmin):
    list_display = ('denuncia', 'autor', 'data')