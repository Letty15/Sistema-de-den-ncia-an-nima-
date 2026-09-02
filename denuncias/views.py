from django.shortcuts import render, redirect
from .models import Denuncia
from .forms import DenunciaForm
import uuid


def listar_denuncia(request):
    denuncias = Denuncia.objects.all()
    return render(request, 'denuncias/listar.html', {'denuncias': denuncias})


def nova_denuncia(request):
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.protocolo = uuid.uuid4().hex[:12].upper()
            denuncia.save()
            return redirect('listar_denuncia')
    else:
        form = DenunciaForm()
    return render(request, 'denuncias/nova_denuncia.html', {'form': form})