from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import inicio

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('denuncias/', include('denuncias.urls')),
    path('respostas/', include('respostas.urls')),
    path('conteudos/', include('conteudos.urls')),
    path('usuarios/', include('usuarios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )