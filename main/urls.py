from django.contrib import admin
from django.urls import path
from core.views import *
import core.views as core_views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", core_views.login, name="login"),
    path('index/', core_views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
