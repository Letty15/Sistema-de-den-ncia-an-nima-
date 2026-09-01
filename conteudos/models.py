from usuarios.models import Usuario
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
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo