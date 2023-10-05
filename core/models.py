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

class Mi_Mascota(models.Model):
    nombre = models.CharField(max_length=255, blank=True , null=True)
    tipo_mascota = models.CharField(max_length=255, blank=True, null=True)
    edad = models.CharField(max_length=255, blank=True, null=True)
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True , null=True)


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
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    foto = models.ImageField(null=True, blank=True, upload_to="media/mascotas")


class Publicaciones(models.Model):
    Gato = 'Gato'
    Perro = 'Perro'
    Perdida_mascota = 'Perdida de mascota'
    Busqueda_mascota = 'Busqueda de mascota'
    Presentacion = 'Presentacion de mascota'
    tipo_mascotas = (
        (Gato, 'Gato'),
        (Perro, 'Perro')
    )

    tipo_publicaciones = (
        (Perdida_mascota, 'Perdida de mascota'),
        (Busqueda_mascota, 'Busqueda de mascota'),
        (Presentacion, 'Presentacion de mascota'),
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

@receiver(post_save, sender=Mascota)
def post_save_mascota(sender, instance, created, **kwargs):
    if created and instance.foto:
        url = "http://68.183.54.183:8090" + instance.foto.url
        openai.api_key = Configuracion.objects.all()[0].token_gpt
        content = """ "Eres experto en identificar animales en fotos, la gente te enviara fotos y tu debes armar un archivo json con la siguiente estructura {'Es_Animal': True, 'Tipo_de_Animal': 'Gato', 'Color': 'Atigrado con tonos grises, blancos y negros', 'Tags': ['#gato', '#felino', '#mascota', '#atigrado', '#doméstico', '#relajado', '#pelaje_mixto']} enfocate solo en los animales de la foto y si la foto no contiene un animal dame el json vacio es importante que solo me respondas el json" """
        prompt_obj = [
            {"role": "system", "content": content},
            {"role": "user", "content": "Esta es la foto " + url},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
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
            print(data["Tags"])
            for tag_name in data["Tags"]:
        
                tag, created = Tag.objects.get_or_create(name=tag_name)
                # Agregar la etiqueta a la instancia de Mascota
                instance.tags.add(tag)

            # Guardar la instancia de Mascota una vez que se han agregado todas las etiquetas
            instance.save()