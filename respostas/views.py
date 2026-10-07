from django.contrib.auth.decorators import login_required
from administracao.decorators import cae_required
from django.shortcuts import get_object_or_404, render, redirect
from denuncias.models import Denuncia
from .models import RespostaDenuncia
from .forms import RespostaForm


# Listar respostas
@login_required
def listar_respostas(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    respostas = denuncia.respostas.all()
    return render(request, 'respostas/listar_respostas.html', {'respostas': respostas, 'denuncia': denuncia})


# Criar resposta
@cae_required
def nova_resposta(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.denuncia = denuncia
            resposta.save()
            return redirect('listar_respostas', protocolo=denuncia.protocolo)
    else:
        form = RespostaForm()
    return render(request, 'respostas/nova_resposta.html', {'form': form, 'denuncia': denuncia})


# Detalhar resposta
@login_required
def detalhar_resposta(request, id):
    resposta = get_object_or_404(RespostaDenuncia, id=id)
    return render(request, 'respostas/detalhar_resposta.html', {'resposta': resposta, 'denuncia': resposta.denuncia})


# Editar resposta
@cae_required
def editar_resposta(request, id):
    resposta = get_object_or_404(RespostaDenuncia, pk=id)
    if request.method == 'POST':
        form = RespostaForm(request.POST, instance=resposta)
        if form.is_valid():
            form.save()
            return redirect('listar_respostas', protocolo=resposta.denuncia.protocolo)
    else:
        form = RespostaForm(instance=resposta)
    return render(request, 'respostas/nova_resposta.html', {
        'form': form,
        'resposta': resposta,
        'denuncia': resposta.denuncia,
    })


# Deletar resposta
@cae_required
def deletar_resposta(request, id):
    resposta = get_object_or_404(RespostaDenuncia, pk=id)
    protocolo = resposta.denuncia.protocolo
    resposta.delete()
    return redirect('listar_respostas', protocolo=protocolo)