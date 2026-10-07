from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import ConteudoEducativo, CanalApoio
from .forms import ConteudoEducativoForm, CanalApoioForm


def listar_conteudo(request):
    conteudos = ConteudoEducativo.objects.all()
    return render(request, 'conteudos/listar.html', {'conteudos': conteudos})

@login_required
@permission_required('conteudos.add_conteudoeducativo', raise_exception=True)
def novo_conteudo(request):
    if request.method == 'POST':
        form = ConteudoEducativoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_conteudo')
    else:
        form = ConteudoEducativoForm()
    return render(request, 'conteudos/novo_conteudo.html', {'form': form})


def detalhar_conteudo(request, pk):
    conteudo = get_object_or_404(ConteudoEducativo, pk=pk)
    return render(request, 'conteudos/detalhar_conteudo.html', {'conteudo': conteudo})

@login_required
@permission_required('conteudos.change_conteudoeducativo', raise_exception=True)
def editar_conteudo(request, pk):
    conteudo = get_object_or_404(ConteudoEducativo, pk=pk)
    if request.method == 'POST':
        form = ConteudoEducativoForm(request.POST, instance=conteudo)
        if form.is_valid():
            form.save()
            return redirect('detalhar_conteudo', pk=conteudo.pk)
    else:
        form = ConteudoEducativoForm(instance=conteudo)
    return render(request, 'conteudos/editar_conteudo.html', {'form': form, 'conteudo': conteudo})

@login_required
@permission_required('conteudos.delete_conteudoeducativo', raise_exception=True)
def deletar_conteudo(request, pk):
    conteudo = get_object_or_404(ConteudoEducativo, pk=pk)
    if request.method == 'POST':
        conteudo.delete()
        return redirect('listar_conteudo')
    return render(request, 'conteudos/deletar_conteudo.html', {'conteudo': conteudo})


def listar_canal(request):
    canais = CanalApoio.objects.all()
    return render(request, 'conteudos/listar_canal.html', {'canais': canais})

@login_required
@permission_required('conteudos.add_canalapoio', raise_exception=True)
def novo_canal(request):
    if request.method == 'POST':
        form = CanalApoioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_canal')
    else:
        form = CanalApoioForm()
    return render(request, 'conteudos/novo_canal.html', {'form': form})

def detalhar_canal(request, pk):
    canal = get_object_or_404(CanalApoio, pk=pk)
    return render(request, 'conteudos/detalhar_canal.html', {'canal': canal})

@login_required
@permission_required('conteudos.change_canalapoio', raise_exception=True)
def editar_canal(request, pk):
    canal = get_object_or_404(CanalApoio, pk=pk)
    if request.method == 'POST':
        form = CanalApoioForm(request.POST, instance=canal)
        if form.is_valid():
            form.save()
            return redirect('detalhar_canal', pk=canal.pk)
    else:
        form = CanalApoioForm(instance=canal)
    return render(request, 'conteudos/editar_canal.html', {'form': form, 'canal': canal})

@login_required
@permission_required('conteudos.delete_canalapoio', raise_exception=True)
def deletar_canal(request, pk):
    canal = get_object_or_404(CanalApoio, pk=pk)
    if request.method == 'POST':
        canal.delete()
        return redirect('listar_canal')
    return render(request, 'conteudos/deletar_canal.html', {'canal': canal})