from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib import messages
from django.db import transaction
from usuarios.models import Usuario
from .models import Denuncia, HistoricoStatus
from .forms import DenunciaForm, StatusDenunciaForm
from .regras import eh_dona, pode_ver_denuncia
from .evidencias import (
    MAX_EVIDENCIAS, TAMANHO_MAXIMO_MB,
    validar_evidencias, salvar_evidencias, apagar_arquivos,
)
from django.db.models import Count

PERMISSAO_STATUS = 'denuncias.alterar_status_denuncia'


def _contexto_upload():
    return {'max_evidencias': MAX_EVIDENCIAS, 'tamanho_max': TAMANHO_MAXIMO_MB}


@login_required
@permission_required('denuncias.view_denuncia', raise_exception=True)
def listar_denuncia(request):
    """Só o CAE vê TODAS as denúncias. Aceita ?status= para filtrar."""
    status = request.GET.get('status', '')
    denuncias = (
    Denuncia.objects
    .select_related('tipo_violencia')
    .annotate(total_respostas=Count('respostas'))
    .order_by('-data_registro', '-id')
)
    if status in dict(Denuncia.STATUS_CHOICES):
        denuncias = denuncias.filter(status=status)
    else:
        status = ''
    return render(request, 'denuncias/listar.html', {
        'denuncias': denuncias,
        'status_opcoes': Denuncia.STATUS_CHOICES,
        'status_atual': status,
    })


@login_required
def minhas_denuncias(request):
    """Qualquer usuária logada vê só as denúncias que ela mesma registrou."""

    denuncias = (
        Denuncia.objects
        .filter(denunciante_id=request.user.id)
        .select_related('tipo_violencia')
        .order_by('-data_registro', '-id')
    )

    return render(
        request,
        'denuncias/minhas_denuncias.html',
        {'denuncias': denuncias}
    )


@login_required
@permission_required('denuncias.add_denuncia', raise_exception=True)
def nova_denuncia(request):
    try:
        denunciante = request.user.usuario
    except Usuario.DoesNotExist:
        messages.error(request, 'Sua conta não tem um perfil de denunciante associado.')
        return redirect('listar_conteudo')

    erros_evidencia = []
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        try:
            evidencias = validar_evidencias(request.FILES.getlist('evidencias'))
        except ValidationError as e:
            evidencias, erros_evidencia = [], e.messages

        if form.is_valid() and not erros_evidencia:
            with transaction.atomic():
                denuncia = form.save(commit=False)
                denuncia.denunciante = denunciante
                denuncia.save()
                salvar_evidencias(denuncia, evidencias)
            return redirect('denuncia_enviada', protocolo=denuncia.protocolo)
    else:
        form = DenunciaForm()

    return render(request, 'denuncias/form_denuncia.html', {
        'form': form,
        'erros_evidencia': erros_evidencia,
        **_contexto_upload(),
    })


@login_required

def detalhar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)

    if not pode_ver_denuncia(request.user, denuncia):
        raise PermissionDenied

    return render(request, 'denuncias/detalhar_denuncia.html', {
        'denuncia': denuncia,
        'evidencias': denuncia.evidencias.all(),
        'eh_cae': request.user.has_perm(PERMISSAO_STATUS),

        'historico': denuncia.historico_status.select_related(
            'alterado_por'
        ).all(),
    })


@login_required
@permission_required('denuncias.change_denuncia', raise_exception=True)
def editar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if not eh_dona(request.user, denuncia):
        raise PermissionDenied

    atuais = denuncia.evidencias.all()
    erros_evidencia = []

    if request.method == 'POST':
        form = DenunciaForm(request.POST, instance=denuncia)

        ids = [i for i in request.POST.getlist('remover_evidencias') if i.isdigit()]
        a_remover = list(atuais.filter(pk__in=ids))
        try:
            novas = validar_evidencias(
                request.FILES.getlist('evidencias'),
                ja_existentes=atuais.count() - len(a_remover),
            )
        except ValidationError as e:
            novas, erros_evidencia = [], e.messages

        if form.is_valid() and not erros_evidencia:
            with transaction.atomic():
                form.save()
                for imagem in a_remover:
                    imagem.delete()
                salvar_evidencias(denuncia, novas)
            apagar_arquivos(a_remover)
            return redirect('detalhar_denuncia', protocolo=denuncia.protocolo)
    else:
        form = DenunciaForm(instance=denuncia)

    return render(request, 'denuncias/form_denuncia.html', {
        'form': form,
        'denuncia': denuncia,
        'evidencias_atuais': atuais,
        'erros_evidencia': erros_evidencia,
        **_contexto_upload(),
    })


@login_required
@permission_required('denuncias.delete_denuncia', raise_exception=True)
def deletar_denuncia(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if not eh_dona(request.user, denuncia):
        raise PermissionDenied

    if request.method == 'POST':
        imagens = list(denuncia.evidencias.all())
        denuncia.delete()
        apagar_arquivos(imagens)
        return redirect('minhas_denuncias')
    return render(request, 'denuncias/deletar_denuncia.html', {'denuncia': denuncia})


@login_required
@permission_required(PERMISSAO_STATUS, raise_exception=True)
def alterar_status_denuncia(request, protocolo):
    """A CAE atualiza o andamento da denúncia."""

    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)

    if request.method == 'POST':
        status_anterior = denuncia.status

        form = StatusDenunciaForm(
            request.POST,
            instance=denuncia
        )

        if form.is_valid():
            novo_status = form.cleaned_data['status']

            if novo_status != status_anterior:
                with transaction.atomic():
                    form.save()

                    HistoricoStatus.objects.create(
                        denuncia=denuncia,
                        status_anterior=status_anterior,
                        novo_status=novo_status,
                        alterado_por=request.user
                    )

                messages.success(
                    request,
                    'Status atualizado e histórico registrado.'
                )
            else:
                messages.info(
                    request,
                    'O status selecionado já está definido.'
                )

            return redirect(
                'detalhar_denuncia',
                protocolo=denuncia.protocolo
            )

    else:
        form = StatusDenunciaForm(instance=denuncia)

    return render(
        request,
        'denuncias/alterar_status_denuncia.html',
        {
            'form': form,
            'denuncia': denuncia,
        }
    )

@login_required
def denuncia_enviada(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if not eh_dona(request.user, denuncia):
        raise PermissionDenied
    return render(request, 'denuncias/denuncia_enviada.html', {'denuncia': denuncia})