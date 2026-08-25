from django.contrib import admin
from .models import ConteudoEducativo, CanalApoio


@admin.register(ConteudoEducativo)
class ConteudoEducativoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'publicado_em', 'autor')
    list_filter = ('categoria',)
    filter_horizontal = ('canais_apoio',)


admin.site.register(CanalApoio)