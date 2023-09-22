from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from core.models import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login as login_f
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import User
from PIL import Image
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import urllib
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView



class CreatePublicaciones(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        response={}
        color = request.data.get("color")
        tipo_mascota = request.data.get("tipo_mascota")
        descripcion = request.data.get("descripcion")
        foto_mascota = request.FILES.get("foto_mascota")
        tipo_publicacion = request.data.get("tipo_publicacion")
        comentarios = request.data.get("comentarios")

        publicacion = Publicaciones.objects.create(
            color=color,
            tipo_mascota=tipo_mascota,
            descripcion=descripcion,
            foto_mascota=foto_mascota,
            tipo_publicacion=tipo_publicacion,
            comentarios=comentarios,
        )
        publicacion.save()
        return Response(response)
    
class GetAllPublicaciones(APIView):
    def get(self, request, format=None):
        publicaciones = Publicaciones.objects.all()
        serialized_publicaciones = [{
            "color": publicacion.color,
            "tipo_mascota": publicacion.tipo_mascota,
            "descripcion": publicacion.descripcion,
            "tipo_publicacion": publicacion.tipo_publicacion,
            "comentarios": publicacion.comentarios,
            "foto_mascota": publicacion.foto_mascota.url if publicacion.foto_mascota else None,
            "usuario": {
                "id": publicacion.usuario.user.id if publicacion.usuario else None,
                "username": publicacion.usuario.user.username if publicacion.usuario else None,
                "first_name": publicacion.usuario.user.first_name if publicacion.usuario else None,
                "last_name": publicacion.usuario.user.last_name if publicacion.usuario else None,
                "comuna" : publicacion.usuario.comuna if publicacion.usuario else None,
            },
            "id": publicacion.pk,
        } for publicacion in publicaciones]
        return Response(serialized_publicaciones)

    
class GetPublicaciones(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        response = {}
        publicaciones = Publicaciones.objects.all()
        response["publicaciones"] = publicaciones
        return Response(response)