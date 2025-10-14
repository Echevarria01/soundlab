from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Si querés agregar campos personalizados, podés hacerlo acá
    # ejemplo:
    # telefono = models.CharField(max_length=20, blank=True, null=True)
    pass

    def __str__(self):
        return self.username
