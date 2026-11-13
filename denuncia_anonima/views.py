from django.db.models import Count, Q
from django.shortcuts import render

from denuncias.models import Denuncia


def inicio(request):
    """Página inicial. O CAE também vê o painel com números e denúncias recentes."""
    contexto = {}

    if request.user.is_authenticated and request.user.has_perm('denuncias.view_denuncia'):
        contexto['numeros'] = Denuncia.objects.aggregate(
            total=Count('id'),
            pendentes=Count('id', filter=Q(status='pendente')),
            andamento=Count('id', filter=Q(status__in=['em_analise', 'encaminhada'])),
            concluidas=Count('id', filter=Q(status='concluida')),
        )
        contexto['recentes'] = (
            Denuncia.objects.select_related('tipo_violencia')
            .order_by('-data_registro', '-id')[:5]
        )

    return render(request, 'inicio.html', contexto)