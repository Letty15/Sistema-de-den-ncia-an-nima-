from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from denuncias.models import Denuncia
from denuncias.regras import pode_ver_denuncia
from usuarios.models import Usuario
from .models import RespostaDenuncia
from .forms import RespostaForm


# Listar respostas
@login_required
@permission_required('respostas.view_respostadenuncia', raise_exception=True)
def listar_respostas(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if not pode_ver_denuncia(request.user, denuncia):
        raise PermissionDenied
    respostas = denuncia.respostas.all()
    return render(request, 'respostas/listar_respostas.html', {'respostas': respostas, 'denuncia': denuncia})


# Criar 
@login_required
@permission_required('respostas.add_respostadenuncia', raise_exception=True)
def nova_resposta(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.denuncia = denuncia
            resposta.autor = Usuario.objects.filter(pk=request.user.pk).first()
            resposta.save()
            messages.success(request, 'Resposta registrada.')
            return redirect('listar_respostas', protocolo=denuncia.protocolo)
    else:
        form = RespostaForm()
    return render(request, 'respostas/nova_resposta.html', {'form': form, 'denuncia': denuncia})


# Detalhar resposta
@login_required
@permission_required('respostas.view_respostadenuncia', raise_exception=True)
def detalhar_resposta(request, id):
    resposta = get_object_or_404(RespostaDenuncia, id=id)
    if not pode_ver_denuncia(request.user, resposta.denuncia):
        raise PermissionDenied
    return render(request, 'respostas/detalhar_resposta.html', {'resposta': resposta, 'denuncia': resposta.denuncia})


# Editar resposta
@login_required
@permission_required('respostas.change_respostadenuncia', raise_exception=True)
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


@login_required
@permission_required('respostas.delete_respostadenuncia', raise_exception=True)
def deletar_resposta(request, id):
    resposta = get_object_or_404(RespostaDenuncia, pk=id)
    protocolo = resposta.denuncia.protocolo
    if request.method == 'POST':
        resposta.delete()
        messages.success(request, 'Resposta excluída.')
        return redirect('listar_respostas', protocolo=protocolo)
    return render(request, 'respostas/deletar_resposta.html', {'resposta': resposta})