from django.urls import path
from . import views

urlpatterns = [
    path('listar_respostas/<str:protocolo>/', views.listar_respostas, name='listar_respostas'),
    path('nova_resposta/<str:protocolo>/', views.nova_resposta, name='nova_resposta'),
]