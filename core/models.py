from django.db import models
from django.contrib.auth.models import User
import openai
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from django.db import transaction
from django.conf import settings  # Importa esta si aún no lo has hecho


TipoUsuarios = (
    ("0",'Administrador'),
    ("1",'Usuario Comun')
)

class Configuracion(models.Model):
    token_gpt = models.TextField(null=True, blank=True)

class Usuario(models.Model):
    tipo_usuario = models.CharField(max_length=1, choices=TipoUsuarios, default=1)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    comuna = models.CharField(max_length=255, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, max_length=50, on_delete=models.CASCADE, default='UserPrueba')
    active = models.BooleanField(default=True)
    foto = models.ImageField(null=True, blank=True, upload_to="media/usuario")

class Vacuna(models.Model):
    peso = models.CharField(max_length=255, blank=True , null=True)
    nombre_vacuna = models.CharField(max_length=255, blank=True , null=True)
    fecha_aplicacion = models.DateTimeField(null=True, blank=True)
    fecha_proxima_vacuna = models.DateTimeField(null=True, blank=True)


class Mi_Mascota(models.Model):
    nombre = models.CharField(max_length=255, blank=True , null=True)
    tipo_mascota = models.CharField(max_length=255, blank=True, null=True)
    edad = models.CharField(max_length=255, blank=True, null=True)
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True , null=True)
    foto = models.ImageField(null=True, blank=True, upload_to="media/mi_mascota")
    vacunas = models.ManyToManyField(Vacuna, blank=True)
    tags = models.ManyToManyField("Tag",blank=True, null=True)

class FichaMedica(models.Model):
    mascota = models.ForeignKey(Mi_Mascota, on_delete=models.CASCADE)
    fecha_consulta = models.DateTimeField(null=True, blank=True)
    diagnostico = models.TextField(null=True, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Publicaciones(models.Model):
    Gato = 'Gato'
    Perro = 'Perro'
    Perdida_mascota = 'Perdida de mascota'
    tipo_mascotas = (
        (Gato, 'Gato'),
        (Perro, 'Perro')
    )

    tipo_publicaciones = (
        (Perdida_mascota, 'Perdida de mascota'),
    )

    tipo_mascota = models.CharField(max_length=255, choices=tipo_mascotas, default=Perro)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    foto_mascota = models.ImageField(null=True, blank=True, upload_to="media/")
    tipo_publicacion = models.CharField(max_length=255, choices=tipo_publicaciones, default=Perdida_mascota)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

class Comentarios(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

class Servicios(models.Model):

    tipo_servicio = (
        ("Peluqueria", 'Peluqueria'),
        ("Veterinaria", 'Veterinaria'),
        ("Petshop", 'PetShop'),
    )

    nombre = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    latitud = models.CharField(max_length=255, blank=True, null=True)
    longitud = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=255, choices=tipo_servicio, blank=True, null=True)

class Similitud(models.Model):
    publicacion_usuario = models.ForeignKey(Publicaciones, on_delete=models.CASCADE,blank=True, null=True, related_name='similitudes_usuario')
    publicacion_comparada = models.ForeignKey(Publicaciones, on_delete=models.CASCADE,blank=True, null=True, related_name='similitudes_comparadas')
    similitud = models.FloatField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)




            

