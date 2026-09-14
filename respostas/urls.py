from django.urls import path
from . import views

urlpatterns = [
    path('listar_respostas/<str:protocolo>/', views.listar_respostas, name='listar_respostas'),
    path('nova_resposta/<str:protocolo>/', views.nova_resposta, name='nova_resposta'),
    path('detalhar_resposta/<int:id>/', views.detalhar_resposta, name='detalhar_resposta'),
    path('deletar_resposta/<int:id>/', views.deletar_resposta, name='deletar_resposta'),
    path('editar_resposta/<int:id>/', views.editar_resposta, name='editar_resposta'),
]