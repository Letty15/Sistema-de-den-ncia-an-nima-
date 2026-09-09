from django.contrib.auth.models import User
from django.db import models

class Usuario(User):
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, unique=True)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.username