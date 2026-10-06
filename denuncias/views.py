from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from administracao.decorators import cae_required
from usuarios.models import Usuario
from .models import Denuncia
from .forms import DenunciaForm


@cae_required
def listar_denuncia(request):
    """Só o CAE vê TODAS as denúncias (somente leitura)."""
    denuncias = Denuncia.objects.all()
    return render(request, 'denuncias/listar.html', {'denuncias': denuncias})


@login_required
def minhas_denuncias(request):
    """Qualquer usuária logada vê só as denúncias que ela mesma registrou."""
    denuncias = Denuncia.objects.filter(denunciante_id=request.user.id)
    return render(request, 'denuncias/minhas_denuncias.html', {'denuncias': denuncias})


@login_required
def nova_denuncia(request):
    try:
        denunciante = request.user.usuario
    except Usuario.DoesNotExist:
        messages.error(request, 'Sua conta não tem um perfil de denunciante associado.')
        return redirect('listar_conteudo')

    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.denunciante = denunciante
            denuncia.save()
            messages.success(request, f'Denúncia registrada! Protocolo: {denuncia.protocolo}')
            return redirect('detalhar_denuncia', protocolo=denuncia.protocolo)
    else:
        form = DenunciaForm()
    return render(request, 'denuncias/form_denuncia.html', {'form': form})


def _eh_cae(user):
    return user.groups.filter(name='CAE').exists()


def _eh_dona(user, denuncia):
    return denuncia.denunciante_id == user.id


@login_required
def detalhar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if not (_eh_cae(request.user) or _eh_dona(request.user, denuncia)):
        raise PermissionDenied   # vira automaticamente uma página 403
    return render(request, 'denuncias/detalhar_denuncia.html', {'denuncia': denuncia})


@login_required
def editar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if not _eh_dona(request.user, denuncia):
        raise PermissionDenied   # CAE não entra aqui, só a dona

    if request.method == 'POST':
        form = DenunciaForm(request.POST, instance=denuncia)
        if form.is_valid():
            form.save()
            return redirect('detalhar_denuncia', protocolo=denuncia.protocolo)
    else:
        form = DenunciaForm(instance=denuncia)
    return render(request, 'denuncias/form_denuncia.html', {'form': form, 'denuncia': denuncia})


@login_required
def deletar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if not _eh_dona(request.user, denuncia):
        raise PermissionDenied   # CAE não entra aqui, só a dona

    if request.method == 'POST':
        denuncia.delete()
        return redirect('minhas_denuncias')
    return render(request, 'denuncias/deletar_denuncia.html', {'denuncia': denuncia})