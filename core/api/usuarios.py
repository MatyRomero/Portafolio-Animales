from django.shortcuts import render, redirect

# Create your views here.
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


class CreateUsuarios(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        response={}
        user = User.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            email=request.data["email"],
            username=request.data["email"],
            password=request.data["password"],
        )
        user.set_password(request.data["password"])
        user.save()
        usuario = Usuario.objects.create(
            user=user,
            comuna=request.data["comuna"],
            telefono=request.data["telefono"]
        )
        usuario.save()
        return Response(response)
    
class DeleteUsuarios(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        response = {}
        #IT WORKS
        user = User.objects.filter(pk=request.data["id"])[0]

        user.is_active=False
        user.save()
        return Response(response)
    
class EditarUsuarios(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        response = {}
        User.objects.filter(pk = request.data["id_user"]).update(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            email=request.data["email"],
            username=request.data["email"]
        )
        Usuario.objects.filter(pk = request.data["id_usuario"]).update(
            active = request.data["active"],
            telefono = request.data["telefono"]
        )
        return Response(response)

class SetProfileInformation(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        response = {}
        if " " in request.data["nombre"]:
            request.user.first_name = request.data["nombre"].split(" ")[0]
            request.user.last_name = request.data["nombre"].split(" ")[1]
        else:
            request.user.first_name = request.data["nombre"]
        request.user.email = request.data["email"]
        request.user.save()
        request.user.usuario.telefono = request.data["telefono"]
        request.user.usuario.direccion = request.data["direccion"]
        request.user.usuario.comuna = request.data["comuna"]
        request.user.usuario.save()
        return Response(response)
    
class UploadProfilePhoto(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        response = {}
        # Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        # Obtén el objeto Usuario relacionado con el usuario autenticado
        usuario = Usuario.objects.get(user=request.user)
        # Procesa y guarda la foto si se proporciona
        if 'foto' in request.data:
            usuario.foto = request.data['foto']
            usuario.save()
            return Response({"message": "Foto de perfil actualizada con éxito."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No se proporcionó ninguna foto."}, status=status.HTTP_400_BAD_REQUEST)


