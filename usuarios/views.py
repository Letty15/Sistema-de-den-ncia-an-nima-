from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from .forms import CadastroUsuarioForm, EditarUsuarioForm


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuario')
    else:
        form = CadastroUsuarioForm()
    return render(request, 'usuarios/cadastrar_usuario.html', {'form': form})


def listar_usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar.html', {'usuarios': usuarios})


def detalhar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/detalhar_usuario.html', {'usuario': usuario})


def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('detalhar_usuario', pk=usuario.pk)
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})


def deletar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuario')
    return render(request, 'usuarios/deletar_usuario.html', {'usuario': usuario})