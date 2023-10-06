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



class SetPetInformation(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        response = {}
        data = request.data

        # Obtener el objeto Usuario relacionado con el User actual
        usuario, created = Usuario.objects.get_or_create(user=request.user)

        # Recuperar la mascota del usuario actual, si existe, o crear una nueva
        mascota, created = Mi_Mascota.objects.get_or_create(dueño=usuario)

        # Actualizar los campos de la mascota según los datos recibidos
        mascota.nombre = data.get("nombre", mascota.nombre)
        mascota.tipo_mascota = data.get("tipo_mascota", mascota.tipo_mascota)
        mascota.edad = data.get("edad", mascota.edad)

        mascota.save()
        return Response(response, status=status.HTTP_200_OK)
    

class UploadPetPhoto(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        pet_id = request.data.get('pet_id')
        pet = Mi_Mascota.objects.get(pk=pet_id)

        if 'foto' in request.data:
            pet.foto = request.data['foto']
            pet.save()
            return Response({"message": "Foto de la mascota actualizada con éxito."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No se proporcionó ninguna foto."}, status=status.HTTP_400_BAD_REQUEST)


