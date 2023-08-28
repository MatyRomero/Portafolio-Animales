from django.contrib import admin
from django.urls import path
from core.views import *
import core.views as core_views
from core.api import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", core_views.login, name="login"),
    path('index/', core_views.index, name='index'),
    path('registro/', core_views.registro, name='registro'),
    ## API Usuarios
    path("api/create/usuarios", CreateUsuarios.as_view()),
    path("api/edit/usuarios", EditarUsuarios.as_view()),
    path("api/delete/usuarios", DeleteUsuarios.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
