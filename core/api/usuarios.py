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
import requests
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import urllib


from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView

class CreateUsuarios(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        response = {}
        try:
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
            )
            usuario.save()
        except IntegrityError as e:
            if "UNIQUE constraint failed: auth_user.username" in str(e):
                response['error'] = "El correo ya está registrado."
                return Response(response, status=400)
            else:
                response['error'] = "Ocurrió un error en el servidor."
                return Response(response, status=500)

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
        )
        return Response(response)