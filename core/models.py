from django.db import models
from django.contrib.auth.models import User

TipoUsuarios = (
    ("0",'Trabajador'),
    ("1",'Gerente General')
)


class Usuario(models.Model):
    tipo_usuario = models.CharField(max_length=1, choices=TipoUsuarios)
    user = models.OneToOneField(User, max_length=50, on_delete=models.CASCADE, default='UserPrueba')
    active = models.BooleanField(default=True)