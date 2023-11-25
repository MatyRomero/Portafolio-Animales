from django.contrib import admin
from django.db import models
from django.contrib import admin
from core.models import *
from django.utils.html import format_html 
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Publicaciones)
admin.site.register(Comentarios)
admin.site.register(Tag)
admin.site.register(Configuracion)
admin.site.register(Mi_Mascota)
admin.site.register(Vacuna)
admin.site.register(FichaMedica)
admin.site.register(Similitud)