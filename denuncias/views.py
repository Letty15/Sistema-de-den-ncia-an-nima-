from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from usuarios.models import Usuario
from .models import Denuncia
from .forms import DenunciaForm


@login_required
@permission_required('denuncias.view_denuncia', raise_exception=True)
def listar_denuncia(request):
    """Só o CAE vê TODAS as denúncias (somente leitura)."""
    denuncias = Denuncia.objects.all()
    return render(request, 'denuncias/listar.html', {'denuncias': denuncias})


@login_required
@permission_required('denuncias.view_denuncia', raise_exception=True)
def minhas_denuncias(request):
    """Qualquer usuária logada vê só as denúncias que ela mesma registrou."""
    denuncias = Denuncia.objects.filter(denunciante_id=request.user.id)
    return render(request, 'denuncias/minhas_denuncias.html', {'denuncias': denuncias})


@login_required
@permission_required('denuncias.add_denuncia', raise_exception=True)
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

@login_required
@permission_required('denuncias.view_denuncia', raise_exception=True)
def detalhar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    return render(request, 'denuncias/detalhar_denuncia.html', {'denuncia': denuncia})


@login_required
@permission_required('denuncias.change_denuncia', raise_exception=True)
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


@login_required
@permission_required('denuncias.delete_denuncia', raise_exception=True)
def deletar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)

    if request.method == 'POST':
        denuncia.delete()
        return redirect('minhas_denuncias')
    return render(request, 'denuncias/deletar_denuncia.html', {'denuncia': denuncia})