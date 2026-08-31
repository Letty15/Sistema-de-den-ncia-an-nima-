from django.db import models
from denuncias.models import Denuncia
from usuarios.models import Usuario


class RespostaDenuncia(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='respostas')
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='respostas_dadas')
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Resposta à denúncia {self.denuncia.protocolo}'