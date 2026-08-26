from django.db import models
from django.conf import settings

class usuarios(models.Model):
    username= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, unique=True) 
    endereco = models.CharField(max_length=255)


    def __str__(self):
        return self.username.username

# Create your models here.
