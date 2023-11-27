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
from django.db.models import Avg

class VeterinariasCercanasAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # Obtendrías la ubicación actual del usuario de alguna manera, aquí está simulado
        user_lat = request.GET.get('lat', None)
        user_lng = request.GET.get('lng', None)

        if user_lat and user_lng:
            # Aquí harías la lógica para calcular la distancia y obtener las veterinarias más cercanas
            # Por ahora, devolveremos todas las veterinarias ordenadas aleatoriamente como ejemplo
            veterinarias = Servicios.objects.filter(tipo='Veterinaria').annotate(rating_avg=Avg('ratings__value')).order_by('-rating_avg')
            veterinarias_data = [
                {
                    'nombre': veterinaria.nombre,
                    'direccion': veterinaria.direccion,
                    'latitud': veterinaria.latitud,
                    'longitud': veterinaria.longitud,
                    'valoracion_promedio': veterinaria.rating_avg
                } for veterinaria in veterinarias
            ]
            return Response(veterinarias_data)
        else:
            return Response({"error": "Ubicación no proporcionada"}, status=400)
