from django.db import models
from usuarios.models import Usuario

class TipoViolencia(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Denuncia(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('encaminhada', 'Encaminhada ao CAE'),
        ('concluida', 'Concluída'),
    ]
    protocolo = models.CharField(max_length=12, unique=True)
    tipo_violencia = models.ForeignKey(TipoViolencia, on_delete=models.PROTECT, related_name='denuncias')
    denunciante = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='denuncias')
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.protocolo

class Imagem(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='evidencias')
    largura = models.IntegerField()
    altura = models.IntegerField()
    formato = models.CharField(max_length=20)
    dados = models.ImageField(upload_to='evidencias/')
    
# Create your models here.
