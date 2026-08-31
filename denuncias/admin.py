from django.contrib import admin
from .models import TipoViolencia, Denuncia, Imagem

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('protocolo', 'tipo_violencia', 'status', 'data_registro')
    list_filter = ('status', 'tipo_violencia')
    
admin.site.register(TipoViolencia)
admin.site.register(Imagem)

# Register your models here.
