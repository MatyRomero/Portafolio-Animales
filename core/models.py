from django.db import models
from django.contrib.auth.models import User
import openai
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

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

class FichaMedica(models.Model):
    mascota = models.ForeignKey(Mi_Mascota, on_delete=models.CASCADE)
    fecha_consulta = models.DateTimeField(null=True, blank=True)
    diagnostico = models.TextField(null=True, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Mascota(models.Model):
    ES_ANIMAL_CHOICES = [
        (True, 'Sí'),
        (False, 'No'),
    ]

    es_animal = models.BooleanField(null=True, blank=True, choices=ES_ANIMAL_CHOICES, default=True)
    tipo_de_animal = models.CharField(null=True, blank=True, max_length=255)
    color = models.TextField(null=True, blank=True, )
    tags = models.ManyToManyField(Tag, blank=True)
    foto = models.ImageField(null=True, blank=True, upload_to="media/mascotas")


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
        (Busqueda_mascota, 'Busqueda de mascota'),
    )

    tipo_mascota = models.CharField(max_length=255, choices=tipo_mascotas, default=Perro)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    foto_mascota = models.ImageField(null=True, blank=True, upload_to="media/")
    tipo_publicacion = models.CharField(max_length=255, choices=tipo_publicaciones, default=Busqueda_mascota)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)

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

@receiver(post_save, sender=Mascota)
def post_save_mascota(sender, instance, created, **kwargs):
    if created and instance.foto:
        url = "http://68.183.54.183:8090" + instance.foto.url
        openai.api_key = Configuracion.objects.all()[0].token_gpt
        content = """ ""Eres experto en describir fotos de animales , la gente te enviara fotos de animales y solo quiero que describas al animal y me des los siguientes datos es animal si o no , tipo animal , y tags para ese animal descrito devuelveme todo en un json"
        " """
        prompt_obj = [
            {"role": "system", "content": content},
            {"role": "user", "content": "Esta es la foto " + url},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=prompt_obj
        )
        message = response["choices"][0]["message"]
        data = json.loads(message["content"].replace("'", '"'))
        print(data, "esta es la data")
        if len(data) != 0:
            instance.es_animal = data["Es_Animal"]
            instance.tipo_de_animal = data["Tipo_de_Animal"]
            instance.color = data["Color"]
            instance.save()
            print(data, "LLEGO ACA?")
            for tag in data["Tags"]:
                print(data, "LLEGO ACAAAAAA?")
                obj, created = Tag.objects.get_or_create(name=tag)
                instance.tags.add(obj)
            instance.save()