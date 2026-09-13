from django.shortcuts import render, redirect, get_object_or_404
from .models import ConteudoEducativo
from .forms import ConteudoEducativoForm


def listar_conteudo(request):
    conteudos = ConteudoEducativo.objects.all()
    return render(request, 'conteudos/listar.html', {'conteudos': conteudos})


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


def deletar_conteudo(request, pk):
    conteudo = get_object_or_404(ConteudoEducativo, pk=pk)
    if request.method == 'POST':
        conteudo.delete()
        return redirect('listar_conteudo')
    return render(request, 'conteudos/deletar_conteudo.html', {'conteudo': conteudo})