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
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import base64
import uuid

class CreatePublicaciones(APIView):
    def post(self, request):
        response = {}

        # Obtén el usuario autenticado
        usuario = Usuario.objects.get(user=request.user)

        # Recupera los datos de la solicitud
        tipo_mascota = request.data.get("tipo_mascota")
        descripcion = request.data.get("descripcion")
        foto_mascota = request.FILES.get("foto_mascota")

        # Crea la publicación relacionando al usuario actual
        publicacion = Publicaciones.objects.create(
            tipo_mascota=tipo_mascota,
            descripcion=descripcion,
            foto_mascota=foto_mascota,
            usuario=usuario  # Relaciona la publicación con el usuario actual
        )
        publicacion.save()
        return Response({'publicacion_id': publicacion.id}, status=status.HTTP_201_CREATED)

    
class GetAllPublicaciones(APIView):
    def get(self, request, format=None):
        publicaciones = Publicaciones.objects.all().order_by('-id')
        serialized_publicaciones = []

        for publicacion in publicaciones:
            # Obtén todos los comentarios relacionados con esta publicación
            comentarios = Comentarios.objects.filter(publicacion=publicacion)
            # Serializa los comentarios
            serialized_comentarios = [{
                "comentario": comentario.comentario,
                "usuario": {
                    "id": comentario.usuario.user.id if comentario.usuario else None,
                    "username": comentario.usuario.user.username if comentario.usuario else None,
                    "first_name": comentario.usuario.user.first_name if comentario.usuario else None,
                    "last_name": comentario.usuario.user.last_name if comentario.usuario else None,
                    "comuna": comentario.usuario.comuna if comentario.usuario else None,
                },
                "id": comentario.pk,
            } for comentario in comentarios]

            # Serializa la publicación y agrega los comentarios serializados
            serialized_publicacion = {
                "tipo_mascota": publicacion.tipo_mascota,
                "descripcion": publicacion.descripcion,
                "foto_mascota": publicacion.foto_mascota.url if publicacion.foto_mascota else None,
                "fecha": publicacion.fecha,
                "usuario": {
                    "id": publicacion.usuario.user.id if publicacion.usuario else None,
                    "username": publicacion.usuario.user.username if publicacion.usuario else None,
                    "first_name": publicacion.usuario.user.first_name if publicacion.usuario else None,
                    "last_name": publicacion.usuario.user.last_name if publicacion.usuario else None,
                    "comuna": publicacion.usuario.comuna if publicacion.usuario else None,
                },
                "id": publicacion.pk,
                "comentarios": serialized_comentarios,  # Agregar comentarios serializados
            }
            serialized_publicaciones.append(serialized_publicacion)

        return Response(serialized_publicaciones)


    
class GetPublicaciones(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        response = {}
        publicaciones = Publicaciones.objects.all()
        response["publicaciones"] = publicaciones
        return Response(response)


class EliminarPublicacion(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            publicacion_id = request.data.get("id")
            publicacion = Publicaciones.objects.get(pk=publicacion_id)
            publicacion.delete()
            return Response({'mensaje': 'Publicación eliminada correctamente'}, status=status.HTTP_200_OK)
        except Publicaciones.DoesNotExist:
            return Response({'mensaje': 'Publicación no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'mensaje': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class EditarPublicacion(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        publicacion_id = request.data.get('publicacionId')
        descripcion = request.data.get('descripcion')
        foto_mascota = request.FILES.get('foto_mascota') 

        try:
            publicacion = Publicaciones.objects.get(pk=publicacion_id)
            if descripcion:
                publicacion.descripcion = descripcion
            
            if foto_mascota:
                nombre_foto = f'{uuid.uuid4()}.{foto_mascota.name.split(".")[-1]}'
                publicacion.foto_mascota.save(nombre_foto, foto_mascota, save=True)
            else:
                publicacion.save()

            return Response({'mensaje': 'Publicación actualizada correctamente'}, status=status.HTTP_200_OK)

        except Publicaciones.DoesNotExist:
            return Response({'mensaje': 'Publicación no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'mensaje': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    