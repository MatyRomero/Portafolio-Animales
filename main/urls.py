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
    path('publicaciones/', core_views.publicaciones, name='publicaciones'),
    path('veterinarias/', core_views.veterinarias, name='veterinarias'),
    path('peluquerias/', core_views.peluquerias, name='peluquerias'),
    path('shops/', core_views.shops, name='shops'),
    path('perfil/', core_views.perfil, name='perfil'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('ficha_medica/', core_views.ficha, name='ficha_medica'),
    ## API Usuarios
    path("api/create/usuarios", CreateUsuarios.as_view()),
    path("api/edit/usuarios", EditarUsuarios.as_view()),
    path("api/delete/usuarios", DeleteUsuarios.as_view()),
    path("api/internal/set/profile_information", SetProfileInformation.as_view()),
    path('api/actualizar_img/user', UploadProfilePhoto.as_view(), name='upload-profile-photo'),
    ## API Publicaciones
    path("api/create/publicaciones", CreatePublicaciones.as_view()),
    path('api/get_allpublicaciones', GetAllPublicaciones.as_view()),
    ## API Comentarios
    path('api/get_allcomentarios', GetAllComentarios.as_view()),
    path('api/create/comentarios/<int:publicacion_id>/', CreateComentario.as_view()),
    ## API Mi Mascota
    path("api/internal/update/pet_information", SetPetInformation.as_view()),
    path('api/actualizar_img/pet', UploadPetPhoto.as_view(), name='upload-pet-photo'),
    path('api/create/vacunas', CreateVacuna.as_view()),
    path('api/get/vacunas', GetVacunas.as_view()),
    path('api/get/fichamedica', GetFichaMedica.as_view()),
    path('api/create/fichamedica', CreateConsulta.as_view()),
    path('api/create_publicacion/mi_mascota', CreatePublicacionesMiMascota.as_view()),
    path('api/get_mascotas_by_dueño', GetMascotasPorDueno.as_view()),
    path('api/create/mascota', CreateMascota.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
