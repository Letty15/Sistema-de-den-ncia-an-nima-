from django.conf import settings
from django.db import models


class CanalApoio(models.Model):
    nome = models.CharField(max_length=100)       # Disque 180, Disque 100, 190...
    descricao = models.TextField()
    contato = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class ConteudoEducativo(models.Model):
    CATEGORIA_CHOICES = [
        ('direitos', 'Direitos'),
        ('prevencao', 'Prevenção'),
        ('impactos', 'Impactos psicológicos'),
    ]
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    corpo = models.TextField()
    canais_apoio = models.ManyToManyField(CanalApoio, related_name='conteudos', blank=True)
    publicado_em = models.DateTimeField(auto_now_add=True)
    # O autor é sempre um membro da CAE (conta comum do Django, não um Usuario denunciante).
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'groups__name': 'CAE'},
    )

    def __str__(self):
        return self.titulo