from django.db import models
from django.contrib.auth.models import User

TipoUsuarios = (
    ("0",'Administrador'),
    ("1",'Usuario Comun')
)




class Usuario(models.Model):
    tipo_usuario = models.CharField(max_length=1, choices=TipoUsuarios, default=1)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    comuna = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, max_length=50, on_delete=models.CASCADE, default='UserPrueba')
    active = models.BooleanField(default=True)


class Publicaciones(models.Model):
    Gato = 'Gato'
    Perro = 'Perro'
    Perdida_mascota = 'Perdida de mascota'
    Busqueda_mascota = 'Busqueda de mascota'
    tipo_mascotas = (
        (Gato, 'Gato'),
        (Perro, 'Perro')
    )

    tipo_publicaciones = (
        (Perdida_mascota, 'Perdida de mascota'),
        (Busqueda_mascota, 'Busqueda de mascota')
    )

    tipo_mascota = models.CharField(max_length=255, choices=tipo_mascotas, default=Perro)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    foto_mascota = models.ImageField(null=True, blank=True, upload_to="media/")
    tipo_publicacion = models.CharField(max_length=255, choices=tipo_publicaciones, default=Busqueda_mascota)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

class Comentarios(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
