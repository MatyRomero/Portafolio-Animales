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


class ReconocerMascota(APIView):
    def post(self, request, *args, **kwargs):
        imagen_archivo = request.FILES.get('foto')
        if not imagen_archivo:
            return Response({"error": "No se proporcionó archivo de imagen."}, status=400)
        mascota_id = request.data.get('mascota_id')
        if mascota_id:
            mascota = Mascota.objects.get(id=mascota_id)
        else:
            mascota = Mascota.objects.create(foto=imagen_archivo)
        print(request.data)
        url = "http://68.183.54.183:8090" + mascota.foto.url
        openai.api_key = Configuracion.objects.all()[0].token_gpt
        content = """ "Eres experto en identificar animales en fotos, la gente te enviara fotos y tu debes armar un archivo json con la siguiente estructura {'Es_Animal': True, 'Tipo_de_Animal': 'Gato', 'Color': 'Atigrado con tonos grises, blancos y negros', 'Tags': ['#gato', '#felino', '#mascota', '#atigrado', '#domÃ©stico', '#relajado', '#pelaje_mixto']} enfocate solo en los animales de la foto y si la foto no contiene un animal dame el json con cada punto en desconocido es importante que solo me respondas el json, ademas es importante que sepas que este json que te entrego es solo un ejemplo al igual que el de los tag por lo cual esto quiere decir que van a ir cambiando solo quiero que sigas la estructura de este y otro punto importante es que siempre quiero que me respondas o me llenes los tag " """
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
                        mascota.tags.add(tag_obj)
                    print("Tags asociados a la instancia de Mascota:", mascota.tags.all())
                    tags_created = True
                    mascota.es_animal = data.get("Es_Animal", False)
                    mascota.tipo_de_animal = data.get("Tipo_de_Animal", "")
                    mascota.color = data.get("Color", "")
            except json.JSONDecodeError:
                print("Error al decodificar JSON. Reintentando...")
            except Exception as e:
                print(f"Error inesperado: {e}. Reintentando...")
        mascota.save()
        print("FINAL FINAL FINAL" , mascota.tags.all())
        tags_nueva_mascota = set([tag.name for tag in mascota.tags.all()])
        print("Tags de la nueva mascota:", tags_nueva_mascota)
        similitudes = []
        for mascota_existente in Mascota.objects.exclude(id=mascota.id):
            tags_mascota_existente = set([tag.name for tag in mascota_existente.tags.all()])
            print("Comparando con mascota ID:", mascota_existente.id, "| Tags:", tags_mascota_existente)
            
            porcentaje_similitud = calcular_coincidencia_tags(tags_nueva_mascota, tags_mascota_existente)
            print("Porcentaje de similitud con mascota ID", mascota_existente.id, ":", porcentaje_similitud)

            similitudes.append({'mascota_id': mascota_existente.id, 'similitud': porcentaje_similitud})
        similitudes.sort(key=lambda x: x['similitud'], reverse=True)
        print("Similitudes calculadas:", similitudes)
        return Response({
            "mensaje": "Procesamiento completado",
            "tags": [tag.name for tag in mascota.tags.all()],
            "similitudes": similitudes
        })
    
class SimilitudesMascotaView(APIView):
    def get(self, request, mascota_id, *args, **kwargs):
        try:
            mascota = Mascota.objects.get(id=mascota_id)
        except Mascota.DoesNotExist:
            return Response({"error": "Mascota no encontrada."}, status=404)

        tags_nueva_mascota = set([tag.name for tag in mascota.tags.all()])
        similitudes = []

        for mascota_existente in Mascota.objects.exclude(id=mascota.id):
            tags_mascota_existente = set([tag.name for tag in mascota_existente.tags.all()])
            porcentaje_similitud = calcular_coincidencia_tags(tags_nueva_mascota, tags_mascota_existente)
            if porcentaje_similitud >= 55:
                similitudes.append({'mascota_id': mascota_existente.id, 'similitud': porcentaje_similitud})

        return Response({"similitudes": similitudes})