from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, unique=True) 
    endereco = models.CharField(max_length=255)


    def __str__(self):
        return self.user.username

# Create your models here.
