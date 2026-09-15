from django.urls import path
from . import views

urlpatterns = [
    path('listar_denuncia/', views.listar_denuncia, name='listar_denuncia'),
    path('nova_denuncia/', views.nova_denuncia, name='nova_denuncia'),
    path('detalhar_denuncia/<str:protocolo>/', views.detalhar_denuncia, name='detalhar_denuncia'),
    path('editar_denuncia/<str:protocolo>/', views.editar_denuncia, name='editar_denuncia'),
    path('deletar_denuncia/<str:protocolo>/', views.deletar_denuncia, name='deletar_denuncia'),
]