from django.db import models
from django.contrib.auth.models import User

TipoUsuarios = (
    ("0",'Administrador'),
    ("1",'Usuario Comun')
)


class Usuario(models.Model):
    tipo_usuario = models.CharField(max_length=1, choices=TipoUsuarios, default=1)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, max_length=50, on_delete=models.CASCADE, default='UserPrueba')
    active = models.BooleanField(default=True)