from django.urls import path
from . import views

urlpatterns = [
    path('listar_conteudo/', views.listar_conteudo, name='listar_conteudo'),
    path('novo_conteudo/', views.novo_conteudo, name='novo_conteudo'),
    path('detalhar_conteudo/<int:pk>/', views.detalhar_conteudo, name='detalhar_conteudo'),
    path('editar_conteudo/<int:pk>/', views.editar_conteudo, name='editar_conteudo'),
    path('deletar_conteudo/<int:pk>/', views.deletar_conteudo, name='deletar_conteudo'),

    path('listar_canal/', views.listar_canal, name='listar_canal'),
    path('novo_canal/', views.novo_canal, name='novo_canal'),
    path('detalhar_canal/<int:pk>/', views.detalhar_canal, name='detalhar_canal'),
    path('editar_canal/<int:pk>/', views.editar_canal, name='editar_canal'),
    path('deletar_canal/<int:pk>/', views.deletar_canal, name='deletar_canal'),
]