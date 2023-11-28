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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
import openai


def calcular_coincidencia_tags(tags_mascota_1, tags_mascota_2):
    coincidencias = set(tags_mascota_1).intersection(tags_mascota_2)
    total_tags = len(set(tags_mascota_1).union(tags_mascota_2))
    if total_tags == 0:
        return 0
    return len(coincidencias) / total_tags * 100


class ReconocerMascotaPublicacion(APIView):
    def post(self, request, *args, **kwargs):
        imagen_archivo = request.FILES.get('foto')
        if not imagen_archivo:
            return Response({"error": "No se proporcionó archivo de imagen."}, status=400)

        publicacion_id = request.data.get('publicacion_id')
        if not publicacion_id:
            return Response({"error": "No se proporcionó ID de publicación."}, status=400)

        try:
            publicacion = Publicaciones.objects.get(id=publicacion_id)
        except Publicaciones.DoesNotExist:
            return Response({"error": "Publicación no encontrada."}, status=404)

        publicacion.foto_mascota = imagen_archivo
        publicacion.save()
        print(request.data)
        url = "http://68.183.54.183:8090" + publicacion.foto_mascota.url
        openai.api_key = Configuracion.objects.all()[0].token_gpt
        content = """ "Eres experto en identificar animales en fotos, la gente te enviara fotos y tu debes armar un archivo json con la siguiente estructura 'Tags': ['#gato', '#felino', '#mascota', '#atigrado', '#domÃ©stico', '#relajado', '#pelaje_mixto']} enfocate solo en los animales de la foto y si la foto no contiene un animal dame el json con cada punto en desconocido es importante que solo me respondas el json, ademas es importante que sepas que este json que te entrego es solo un ejemplo al igual que el de los tag por lo cual esto quiere decir que van a ir cambiando solo quiero que sigas la estructura de este y otro punto importante es que siempre quiero que me respondas o me llenes los tag " """
        prompt_obj = [
            {"role": "system", "content": content},
            {"role": "user", "content": "Esta es la foto " + url},
        ]
        tags_created = False
        while not tags_created:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-1106",
                    messages=prompt_obj
                )
                message = response["choices"][0]["message"]
                data = json.loads(message["content"].replace("'", '"'))

                if data and len(data) != 0:
                    for tag_name in data.get("Tags", []):
                        print("Procesando tag:", tag_name)
                        tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                        publicacion.tags.add(tag_obj)
                    print("Tags asociados a la instancia de Mascota:", publicacion.tags.all())
                    tags_created = True
            except json.JSONDecodeError:
                print("Error al decodificar JSON. Reintentando...")
            except Exception as e:
                print(f"Error inesperado: {e}. Reintentando...")
        publicacion.save()
        print("FINAL FINAL FINAL" , publicacion.tags.all())
        tags_nueva_publicacion = set([tag.name for tag in publicacion.tags.all()])
        print("Tags de la nueva mascota:", tags_nueva_publicacion)
        similitudes = []
        for publicacion_existente in Publicaciones.objects.exclude(id=publicacion.id):
            print("ID de la publicación actual:", publicacion.id)
            tags_publicacion_existente = set([tag.name for tag in publicacion_existente.tags.all()])
            print("Comparando con publicación ID:", publicacion_existente.id, "| Tags:", tags_publicacion_existente)
            
            porcentaje_similitud = calcular_coincidencia_tags(tags_nueva_publicacion, tags_publicacion_existente)
            print("Porcentaje de similitud con publicación ID", publicacion_existente.id, ":", porcentaje_similitud)

            similitudes.append({'publicacion_id': publicacion_existente.id, 'similitud': porcentaje_similitud})
        similitudes.sort(key=lambda x: x['similitud'], reverse=True)
        print("Similitudes calculadas:", similitudes)
        for s in similitudes:
            Similitud.objects.create(publicacion=publicacion, similitud=s['similitud'])
        return Response({
            "mensaje": "Procesamiento completado",
            "tags": [tag.name for tag in publicacion.tags.all()],
            "similitudes": similitudes
        })
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            publicaciones_usuario = Publicaciones.objects.filter(usuario__user=request.user)
            similitudes = Similitud.objects.filter(publicacion_usuario__in=publicaciones_usuario)
            similitudes = Similitud.objects.filter(
                publicacion_usuario__in=publicaciones_usuario,
                similitud__gt=51.0
            )
            similitudes_data = []

            for s in similitudes:
                nombre_usuario_dueño_publicacion_comparada = s.publicacion_comparada.usuario.user.username

                similitudes_data.append({
                    "publicacion_usuario_id": s.publicacion_usuario.id,
                    "publicacion_comparada_id": s.publicacion_comparada.id,
                    "similitud": s.similitud,
                    "fecha": s.fecha,
                    "usuario_comparado": nombre_usuario_dueño_publicacion_comparada
                })
            return Response({"similitudes": similitudes_data})
        else:
            return Response({"error": "Usuario no autenticado."}, status=status.HTTP_403_FORBIDDEN)
    
class ReconocerMascota(APIView):
    def post(self, request, *args, **kwargs):
        imagen_archivo = request.FILES.get('foto')
        if not imagen_archivo:
            return Response({"error": "No se proporcionó archivo de imagen."}, status=400)

        mi_mascota_id = request.data.get('mi_mascota_id')
        if not mi_mascota_id:
            return Response({"error": "No se proporcionó ID de mi mascota."}, status=400)

        try:
            mi_mascota = Mi_Mascota.objects.get(id=mi_mascota_id)
        except Mi_Mascota.DoesNotExist:
            return Response({"error": "Mi mascota no encontrada."}, status=404)

        mi_mascota.foto = imagen_archivo
        mi_mascota.save()

        url = "http://68.183.54.183:8090" + mi_mascota.foto.url
        openai.api_key = Configuracion.objects.all()[0].token_gpt
        content = """ "Eres experto en identificar animales en fotos, la gente te enviara fotos y tu debes armar un archivo json con la siguiente estructura 'Tags': ['#gato', '#felino', '#mascota', '#atigrado', '#doméstico', '#relajado', '#pelaje_mixto']} enfocate solo en los animales de la foto y si la foto no contiene un animal dame el json con cada punto en desconocido es importante que solo me respondas el json, ademas es importante que sepas que este json que te entrego es solo un ejemplo al igual que el de los tag por lo cual esto quiere decir que van a ir cambiando solo quiero que sigas la estructura de este y otro punto importante es que siempre quiero que me respondas o me llenes los tag " """
        prompt_obj = [
            {"role": "system", "content": content},
            {"role": "user", "content": "Esta es la foto " + url},
        ]
        tags_created = False
        while not tags_created:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-1106",
                    messages=prompt_obj
                )
                message = response["choices"][0]["message"]
                data = json.loads(message["content"].replace("'", '"'))

                if data and len(data) != 0:
                    for tag_name in data.get("Tags", []):
                        tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                        mi_mascota.tags.add(tag_obj)
                    tags_created = True
            except json.JSONDecodeError:
                print("Error al decodificar JSON. Reintentando...")
            except Exception as e:
                print(f"Error inesperado: {e}. Reintentando...")
        mi_mascota.save()
        tags_nueva_mascota = [tag.name for tag in mi_mascota.tags.all()]
        print("Tags de la nueva mascota:", tags_nueva_mascota)

        return Response({
            "mensaje": "Procesamiento completado",
            "tags": tags_nueva_mascota
        })
    
class PublicacionConComentariosView(APIView):
    def get(self, request, publicacion_id):
        # Obtener la publicación
        publicacion = get_object_or_404(Publicaciones, id=publicacion_id)
        
        usuario_info = {
            "first_name": publicacion.usuario.user.first_name,
            "last_name": publicacion.usuario.user.last_name,
            "comuna": publicacion.usuario.comuna,
            "direccion": publicacion.usuario.direccion,
            "telefono": publicacion.usuario.telefono,
        }

        publicacion_data = {
            "id": publicacion.id,
            "usuario": usuario_info,
            "descripcion": publicacion.descripcion,
            "foto_mascota": request.build_absolute_uri(settings.MEDIA_URL + str(publicacion.foto_mascota)) if publicacion.foto_mascota else None,
            "fecha": publicacion.fecha,
        }

        # Obtener los comentarios de la publicación
        comentarios = Comentarios.objects.filter(publicacion_id=publicacion_id).select_related('usuario')
        comentarios_data = [{
            "id": comentario.id,
            "comentario": comentario.comentario,
            "usuario": {
                "first_name": comentario.usuario.user.first_name,
                "last_name": comentario.usuario.user.last_name,
            }
        } for comentario in comentarios]

        # Combinar los datos de la publicación con los comentarios
        response_data = {
            "publicacion": publicacion_data,
            "comentarios": comentarios_data
        }

        return Response(response_data)
