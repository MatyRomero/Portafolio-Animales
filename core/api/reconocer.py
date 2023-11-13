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





class ReconocerMascota(APIView):
    def post(self, request, *args, **kwargs):
        # Obtener la URL de la foto
        imagen_archivo = request.FILES.get('foto')
        if not imagen_archivo:
            return Response({"error": "No se proporcionó archivo de imagen."}, status=400)
        # Obtener o crear la instancia de Mascota
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
        # El resto de tu lógica...
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

        # Devolver una respuesta
        return Response({"mensaje": "Procesamiento completado", "tags": [tag.name for tag in mascota.tags.all()]})