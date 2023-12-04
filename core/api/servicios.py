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
from math import radians, cos, sin, asin, sqrt
import requests


def obtener_peluquerias_animales(lat, lng, api_key):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 10000,  # Radio en metros
        "keyword": "grooming",  # Palabra clave para peluquerías de animales
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()


def obtener_petshops_cercanas(lat, lng, api_key):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 10000,
        "type": "pet_store",
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()


def obtener_veterinarias_cercanas(lat, lng, api_key):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 10000,
        "type": "veterinary_care",
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

def obtener_detalles_del_lugar(place_id, api_key):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": api_key,
        "fields": "name,rating,formatted_address"
    }
    response = requests.get(url, params=params)
    return response.json()

        
class VeterinariasCercanasAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_lat = request.GET.get('lat', None)
        user_lng = request.GET.get('lng', None)
        # api_key = "AIzaSyA0Jbkg892s0MYoUV1nb99FPcuzfgL1O8g"
        api_key = Configuracion.objects.all()[0].token_google_maps

        if user_lat and user_lng:
            resultados = obtener_veterinarias_cercanas(user_lat, user_lng, api_key)
            lugares = resultados.get('results', [])
            detalles_completos = [obtener_detalles_del_lugar(lugar['place_id'], api_key) for lugar in lugares]
            return Response(detalles_completos)
        else:
            return Response({"error": "Ubicación no proporcionada"}, status=400)


class PetShopCercanasAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_lat = request.GET.get('lat', None)
        user_lng = request.GET.get('lng', None)
        # api_key = "AIzaSyA0Jbkg892s0MYoUV1nb99FPcuzfgL1O8g"
        api_key = Configuracion.objects.all()[0].token_google_maps

        if user_lat and user_lng:
            resultados = obtener_petshops_cercanas(user_lat, user_lng, api_key)
            lugares = resultados.get('results', [])
            detalles_completos = [obtener_detalles_del_lugar(lugar['place_id'], api_key) for lugar in lugares]
            return Response(detalles_completos)
        else:
            return Response({"error": "Ubicación no proporcionada"}, status=400)
        

class PeluqueriasCercanasAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_lat = request.GET.get('lat', None)
        user_lng = request.GET.get('lng', None)
        # api_key = "AIzaSyA0Jbkg892s0MYoUV1nb99FPcuzfgL1O8g"
        api_key = Configuracion.objects.all()[0].token_google_maps

        if user_lat and user_lng:
            resultados = obtener_peluquerias_animales(user_lat, user_lng, api_key)
            lugares = resultados.get('results', [])
            detalles_completos = [obtener_detalles_del_lugar(lugar['place_id'], api_key) for lugar in lugares]
            return Response(detalles_completos)
        else:
            return Response({"error": "Ubicación no proporcionada"}, status=400)