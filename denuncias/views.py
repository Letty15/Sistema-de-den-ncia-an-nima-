from django.shortcuts import render, redirect, get_object_or_404
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
    return render(request, 'denuncias/form_denuncia.html', {'form': form})


def detalhar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    return render(request, 'denuncias/detalhar_denuncia.html', {'denuncia': denuncia})


def editar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if request.method == 'POST':
        form = DenunciaForm(request.POST, instance=denuncia)
        if form.is_valid():
            form.save()
            return redirect('detalhar_denuncia', protocolo=denuncia.protocolo)
    else:
        form = DenunciaForm(instance=denuncia)
    return render(request, 'denuncias/form_denuncia.html', {'form': form, 'denuncia': denuncia})


def deletar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    denuncia.delete()
    return redirect('listar_denuncia')