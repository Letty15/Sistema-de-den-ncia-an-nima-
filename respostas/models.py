
from django.conf import settings
from django.db import models
from denuncias.models import Denuncia


class RespostaDenuncia(models.Model):
    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='respostas'
    )

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='respostas_dadas'
    )

    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Resposta à denúncia {self.denuncia.protocolo}'

class Notificacao(models.Model):
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )

    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )

    mensagem = models.CharField(max_length=255)

    lida = models.BooleanField(default=False)

    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return self.mensagem
