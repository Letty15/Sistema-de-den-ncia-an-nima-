from django.urls import path
from . import views

urlpatterns = [
    path('listar_denuncia/', views.listar_denuncia, name='listar_denuncia'),
    path('nova_denuncia/', views.nova_denuncia, name='nova_denuncia'),
]