"""
URL configuration for vigifia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import admin_index  # Importa la vista
from django.shortcuts import render
from . import views

def admin_view(request):
    return render(request, 'admin.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', admin_index, name='admin_index'),  # Página central
    path('fuentes/', include('buscador_fuentes.urls')),
    path('pdfs/', include('gestor_pdfs.urls')),
    path('plantillas/', include('plantillas.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
