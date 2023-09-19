from django.contrib import admin
from django.db import models
from django.contrib import admin
from core.models import *
from django.utils.html import format_html 
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Publicaciones)