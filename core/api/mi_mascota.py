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
        

class CreateVacuna(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        response = {}
        pet_id = request.data.get("pet_id")
        try:
            mascota = Mi_Mascota.objects.get(pk=pet_id)
        except Mi_Mascota.DoesNotExist:
            return Response({"error": "La mascota no existe"}, status=status.HTTP_404_NOT_FOUND)
        vacuna = Vacuna.objects.create(
            peso=request.data["peso"],
            nombre_vacuna=request.data["nombre_vacuna"],
            fecha_aplicacion=request.data["fecha_aplicacion"],
            fecha_proxima_vacuna=request.data["fecha_proxima_vacuna"],
        )
        mascota.vacunas.add(vacuna)
        response["message"] = "Vacuna creada exitosamente y asociada a la mascota."
        return Response(response, status=status.HTTP_201_CREATED)

class GetVacunas(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        response = {}
        pet_id = request.data.get("pet_id")
        try:
            mascota = Mi_Mascota.objects.get(id=pet_id)
        except Mi_Mascota.DoesNotExist:
            return Response({"error": "La mascota no existe"}, status=status.HTTP_404_NOT_FOUND)
        vacunas = Vacuna.objects.filter(mi_mascota=mascota)
        response["vacunas"] = []
        for vacuna in vacunas:
            response["vacunas"].append({
                "peso": vacuna.peso,
                "nombre": vacuna.nombre_vacuna,
                "fecha_aplicacion": vacuna.fecha_aplicacion,
                "fecha_proxima_vacuna": vacuna.fecha_proxima_vacuna,
            })
        return Response(response)

class GetFichaMedica(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        response = {}
        pet_id = request.data.get("pet_id")
        try:
            mascota = Mi_Mascota.objects.get(id=pet_id)
        except Mi_Mascota.DoesNotExist:
            return Response({"error": "La mascota no existe"}, status=status.HTTP_404_NOT_FOUND)
        ficha_medica = FichaMedica.objects.filter(mascota=mascota)
        response["ficha_medica"] = []
        for ficha_medica in ficha_medica:
            response["ficha_medica"].append({
                "fecha_consulta": ficha_medica.fecha_consulta,
                "diagnostico": ficha_medica.diagnostico,
            })
        return Response(response)

class CreateConsulta(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        response = {}
        pet_id = request.data.get("mascota").get("pet_id")
        try:
            mascota = Mi_Mascota.objects.get(pk=pet_id)
        except Mi_Mascota.DoesNotExist:
            return Response({"error": "La mascota no existe"}, status=status.HTTP_404_NOT_FOUND)
        ficha_medica = FichaMedica.objects.create(
            mascota=mascota,
            fecha_consulta=request.data["fecha_consulta"],
            diagnostico=request.data["diagnostico"],
        )
        ficha_medica.save()
        response["message"] = "Ficha médica creada exitosamente y asociada a la mascota."
        return Response(response, status=status.HTTP_201_CREATED)


