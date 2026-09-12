from django.shortcuts import get_object_or_404, render, redirect
from denuncias.models import Denuncia
from .forms import RespostaForm

# Listar respostas
def listar_respostas(request, protocolo):
    # Busca a denúncia pelo protocolo
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    respostas = denuncia.respostas.all()

    return render(request,'respostas/listar_respostas.html', {'respostas': respostas, 'denuncia': denuncia})


# Criar respostas
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



# Create your views here.
