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
from django.db import transaction




class SetPetInformation(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        response = {}

        # Obtén la mascota del usuario actual
        mi_mascota = request.mi_mascota.usuario

        # Procesa los datos de la mascota si existe
        print(request.mi_mascota.usuario)
        if mi_mascota:
            if "nombre_mascota" in request.data:
                mi_mascota.nombre = request.data["nombre_mascota"]
                mi_mascota.tipo_mascota = request.data.get("tipo_mascota", "")
                mi_mascota.edad = request.data.get("edad", "")
                mi_mascota.save()
                response['message'] = 'Los datos de la mascota se han actualizado con éxito.'
                return Response(response, status=status.HTTP_200_OK)
            else:
                response['message'] = 'No se proporcionaron datos para actualizar la mascota.'
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response['message'] = 'No se encontró una mascota asociada a este usuario.'
            return Response(response, status=status.HTTP_404_NOT_FOUND)



