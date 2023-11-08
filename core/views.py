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
from django.db.models.functions import TruncMonth
from django.db.models import Count
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
def index(request ):
    template_name = "index.html"
    context = {}
    context["publicaciones"] = Publicaciones.objects.all()
    context["comentarios"] = Comentarios.objects.all()
    return render(request, template_name, context)

def registro(request):
    template_name = "registro.html"
    context = {}
    context ["usuarios"] = User.objects.all()
    return render(request, template_name, context)

@login_required(login_url='login')
def publicaciones(request):
    template_name = "publicaciones.html"
    context = {}
    return render(request, template_name, context)

@login_required(login_url='login')
def veterinarias(request):
    template_name = "veterinarias.html"
    context = {}
    return render(request, template_name, context)

@login_required(login_url='login')
def peluquerias(request):
    template_name = "peluquerias.html"
    context = {}
    return render(request, template_name, context)

@login_required(login_url='login')
def shops(request):
    template_name = "shops.html"
    context = {}
    return render(request, template_name, context)

@login_required(login_url='login')
def perfil(request):
    template_name = "perfil.html"
    context = {}
    return render(request, template_name, context)

@login_required(login_url='ficha_medica')
def ficha(request):
    template_name = "ficha_medica.html"
    context = {}
    return render(request,template_name,context)

@login_required(login_url='login')
def dashboard(request):
    template_name = "dashboard.html"
    
    num_perros_perdidos = Publicaciones.objects.filter(
        tipo_mascota=Publicaciones.Perro,
        tipo_publicacion=Publicaciones.Perdida_mascota
    ).count()

    num_gatos_perdidos = Publicaciones.objects.filter(
        tipo_mascota=Publicaciones.Gato,
        tipo_publicacion=Publicaciones.Perdida_mascota
    ).count()

    dog_counts, cat_counts = get_counts_by_month()

    perdidas_por_comuna = Publicaciones.objects.filter(
        tipo_publicacion=Publicaciones.Perdida_mascota
    ).values('usuario__comuna').annotate(total=Count('id')).order_by('usuario__comuna')

    comunas = [item['usuario__comuna'] for item in perdidas_por_comuna]
    conteos = [item['total'] for item in perdidas_por_comuna]

    context = {
        'num_perros_perdidos': num_perros_perdidos,
        'num_gatos_perdidos': num_gatos_perdidos,
        'dog_counts': dog_counts,
        'cat_counts': cat_counts,
        'comunas': comunas,
        'conteos': conteos,
    }

    return render(request, template_name, context)

def get_counts_by_month():
    # Filtrar publicaciones de perdidas por mes y contarlas
    counts_per_month = Publicaciones.objects.filter(
        tipo_publicacion=Publicaciones.Perdida_mascota
    ).annotate(
        month=TruncMonth('fecha')
    ).values(
        'month', 'tipo_mascota'
    ).order_by(
        'month'
    ).annotate(
        count=Count('id')
    )
    
    # Inicializar conteos
    dog_counts = [0] * 12
    cat_counts = [0] * 12

    # Poblar conteos
    for entry in counts_per_month:
        month_index = entry['month'].month - 1  # Obtener el índice del mes (0 para Enero, 1 para Febrero, etc.)
        if entry['tipo_mascota'] == Publicaciones.Gato:
            cat_counts[month_index] = entry['count']
        elif entry['tipo_mascota'] == Publicaciones.Perro:
            dog_counts[month_index] = entry['count']
    
    return dog_counts, cat_counts
