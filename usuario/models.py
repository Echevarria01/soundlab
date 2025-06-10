from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Podés agregar campos extra si querés, por ahora lo dejamos básico
    pass

    def __str__(self):
        return self.username
from django.db import models

# Create your models here.
