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
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


class GetAllComentarios(APIView):
    def get(self, request, format=None):
        comentarios = Comentarios.objects.all().order_by('-id')
        serialized_comentarios = []

        for comentario in comentarios:
            serialized_comentario = {
                "comentario": comentario.comentario,
                "usuario": {
                    "id": comentario.usuario.user.id if comentario.usuario else None,
                    "username": comentario.usuario.user.username if comentario.usuario else None,
                    "first_name": comentario.usuario.user.first_name if comentario.usuario else None,
                    "last_name": comentario.usuario.user.last_name if comentario.usuario else None,
                    "comuna" : comentario.usuario.comuna if comentario.usuario else None,
                },
                "id": comentario.pk,
                "publicacion_id": comentario.publicacion.id,  # Agregamos el ID de la publicación a la que pertenece
            }
            serialized_comentarios.append(serialized_comentario)

        return Response(serialized_comentarios)

class CreateComentario(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, publicacion_id):
        comentario_texto = request.data.get("comentario")

        # Obtener el usuario autenticado
        usuario = request.user.usuario  # Accede al modelo Usuario a través del perfil de usuario autenticado

        try:
            # Obtener la publicación a la que se refiere el comentario
            publicacion = Publicaciones.objects.get(pk=publicacion_id)
        except Publicaciones.DoesNotExist:
            return Response({"error": "La publicación no existe."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el comentario relacionándolo con la publicación y el usuario
        comentario = Comentarios(comentario=comentario_texto, usuario=usuario, publicacion=publicacion)
        comentario.save()

        return Response({"message": "Comentario creado con éxito."}, status=status.HTTP_201_CREATED)

