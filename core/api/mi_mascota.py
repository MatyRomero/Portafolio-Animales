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




class SetPetInformation(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        response = {}
        data = request.data
        print(request.data)
        # Obtener el objeto Usuario relacionado con el User actual
        usuario = Usuario.objects.get_or_create(user=request.user)
        # Recibir el ID de la mascota a actualizar desde el request
        pet_id = int(request.data.get('pet_id'))
        mascota = Mi_Mascota.objects.get(id=pet_id)
        if not pet_id:
            return Response({"detail": "Se requiere el ID de la mascota para la actualización."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            mascota = Mi_Mascota.objects.get(id=pet_id)
        except Mi_Mascota.DoesNotExist:
            return Response({"detail": "Mascota no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar los campos de la mascota según los datos recibidos
        mascota.nombre = request.data.get('nombre')
        mascota.tipo_mascota = request.data.get('tipo_mascota')
        mascota.edad = request.data.get('edad')
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
        pet_id = request.data.get("mi_mascota", {}).get("pet_id")
        if not pet_id:
            return Response({"error": "Pet ID no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            mascota = Mi_Mascota.objects.get(pk=pet_id)
        except Mi_Mascota.DoesNotExist:
            return Response({"error": "La mascota no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        # Asegúrate de validar y limpiar los datos antes de usarlos
        try:
            peso = float(request.data.get("peso"))
        except ValueError:
            return Response({"error": "Peso inválido"}, status=status.HTTP_400_BAD_REQUEST)

        nombre_vacuna = request.data.get("nombre_vacuna")
        fecha_aplicacion = request.data.get("fecha_aplicacion")
        fecha_proxima_vacuna = request.data.get("fecha_proxima_vacuna")

        vacuna = Vacuna.objects.create(
            peso=peso,
            nombre_vacuna=nombre_vacuna,
            fecha_aplicacion=fecha_aplicacion,
            fecha_proxima_vacuna=fecha_proxima_vacuna,
        )
        mascota.vacunas.add(vacuna)
        
        return Response({"message": "Vacuna creada exitosamente y asociada a la mascota."}, status=status.HTTP_201_CREATED)

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
                "id":ficha_medica.id
            })
        print(response)
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
    
class CreatePublicacionesMiMascota(APIView):
    def post(self, request):
        response = {}
        # Obtén el usuario autenticado
        usuario = Usuario.objects.get(user=request.user)
        # Recupera los datos de la solicitud
        tipo_mascota = request.data.get("tipo_mascota")
        descripcion = request.data.get("descripcion")
        foto_mascota = request.FILES.get("foto_mascota")
        tipo_publicacion = request.data.get("tipo_publicacion")
        # Siempre estableceremos 'Busqueda de mascota' como el tipo de publicación
        tipo_publicacion = Publicaciones.Perdida_mascota
        # Crear la publicación relacionando al usuario actual
        publicacion = Publicaciones(
            tipo_mascota=tipo_mascota,
            descripcion=descripcion,
            foto_mascota=foto_mascota,
            tipo_publicacion=tipo_publicacion,
            usuario=usuario
        )
        publicacion.save()
        return Response(response, status=status.HTTP_201_CREATED)

class GetMascotasPorDueno(APIView):
    def post(self, request, format=None):
        user_id = request.data.get('id')
        
        if not user_id:
            return Response({"error": "ID de usuario no proporcionado"}, status=400)

        try:
            usuario = Usuario.objects.get(user_id=user_id)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=404)

        mascotas = Mi_Mascota.objects.filter(dueño=usuario)
        response = {
            "mascotas": [
                {
                    "nombre": mascota.nombre,
                    "tipo_mascota": mascota.tipo_mascota,
                    "edad": mascota.edad,
                    "pet_id":mascota.id,
                    "foto": mascota.foto.url if mascota.foto else None
                } for mascota in mascotas
            ]
        }
        return Response(response)

class CreateMascota(APIView):
    def post(self, request):
        response = {}
        usuario = Usuario.objects.get(user=request.user)

        nombre = request.data.get("nombre")
        tipo_mascota = request.data.get("tipo_mascota")
        edad = request.data.get("edad")
        foto = request.FILES.get("foto")

        mascota = Mi_Mascota(
            nombre=nombre,
            tipo_mascota=tipo_mascota,
            edad=edad,
            foto=foto,
            dueño=usuario
        )
        mascota.save()
        return Response({'mascota_id': mascota.id}, status=status.HTTP_201_CREATED)


class DetalleFichaMedica(APIView):
    def get(self, request, ficha_medica_id):
        ficha = get_object_or_404(FichaMedica, pk=ficha_medica_id)
        mascota = ficha.mascota
        propietario = mascota.dueño if mascota.dueño else None

        data = {
            'Nombre Mascota': mascota.nombre,
            'Tipo Animal': mascota.tipo_mascota,
            'Propietario': propietario.user.username if propietario else '',
            'Fecha': ficha.fecha_consulta.strftime('%Y-%m-%d %H:%M') if ficha.fecha_consulta else '',
            'Edad': mascota.edad,
            'Telefono': propietario.telefono if propietario else '',
            'Diagnostico': ficha.diagnostico,
        }
        print(ficha)
        print(mascota.nombre)
        print(data)
        print(request)
        return Response(data, status=status.HTTP_200_OK)
    
class EliminarMimascota(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            mascota_id = request.data.get("id")
            mascota = Mi_Mascota.objects.get(pk=mascota_id)
            mascota.delete()
            return Response({'mensaje': 'mascota eliminada correctamente'}, status=status.HTTP_200_OK)
        except Publicaciones.DoesNotExist:
            return Response({'mensaje': 'mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'mensaje': str(e)}, status=status.HTTP_400_BAD_REQUEST)

