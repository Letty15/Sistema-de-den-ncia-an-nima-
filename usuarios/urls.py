from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('listar_usuario/', views.listar_usuario, name='listar_usuario'),
    path('detalhar_usuario/<int:pk>/', views.detalhar_usuario, name='detalhar_usuario'),
    path('editar_usuario/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('deletar_usuario/<int:pk>/', views.deletar_usuario, name='deletar_usuario'),
]