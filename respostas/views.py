from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from denuncias.models import Denuncia
from .models import RespostaDenuncia
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


# Detalhar resposta
def detalhar_resposta(request, id):
    resposta = get_object_or_404(RespostaDenuncia, id=id)
    return render(request, "respostas/detalhar_resposta.html", {"resposta": resposta, "denuncia": resposta.denuncia})


# Deletar resposta
def deletar_resposta(request, id):
    resposta = RespostaDenuncia.objects.get(pk = id)
    protocolo = resposta.denuncia.protocolo 
    resposta.delete()
    return redirect("listar_respostas", protocolo=protocolo)


# Editar resposta
def editar_resposta(request, id):
    resposta = get_object_or_404(RespostaDenuncia, pk=id)
    if request.method == "POST":
        form = RespostaForm(request.POST, instance=resposta)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.save()
            # força string e garante que não seja vazio
            protocolo = str(resposta.denuncia.protocolo).strip()
            if not protocolo:
                protocolo = str(resposta.denuncia.id)  # fallback
            return redirect('listar_respostas', protocolo=protocolo)
    else:
        form = RespostaForm(instance=resposta)
    return render(request, "respostas/nova_resposta.html", {
    "form": form,
    "resposta": resposta,
    "denuncia": resposta.denuncia
})




# Create your views here.
