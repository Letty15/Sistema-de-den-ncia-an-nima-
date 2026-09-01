from django.shortcuts import render, redirect, get_object_or_404
from .models import Denuncia, Usuario

def listar_denuncia(request):
    usuario = Usuario.objects.get(user=request.user)
    denuncias = Denuncia.objects.filter(denunciante=usuario)
    return render(request, 'denuncias/listar.html', {'denuncias': denuncias})


# Create your views here.
