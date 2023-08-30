from django.http import JsonResponse

from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import authentication, permissions
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from core.models import *
from django.contrib.auth import login as login_f
# Create your views here.

def login(request):
    template_name = "login.html"
    context = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        # Obtener el valor de la opción "Recuérdame"
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)
            login_f(request, user)
            return redirect("index")
        else:
            logout(request)
    context['remember_me'] = request.POST.get('remember_me')
    return render(request, template_name, context)

@login_required(login_url='login')
def index(request):
    template_name = "index.html"
    context = {}
    return render(request, template_name, context)

def registro(request):
    template_name = "registro.html"
    context = {}
    context ["usuarios"] = User.objects.all()
    return render(request, template_name, context)