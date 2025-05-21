from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import admin_index
from django.shortcuts import redirect
from .views import supabase_register, supabase_login, supabase_logout, admin_users

# 👇 Importamos las vistas de autenticación
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página principal
    path('panel/', admin_index, name='admin_index'),

    # Rutas por app
    path('fuentes/', include('buscador_fuentes.urls')),
    path('pdfs/', include('gestor_pdfs.urls')),
    path('plantillas/', include('plantillas.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('editor/', include('editor.urls')),

    # 🔐 Autenticación
    path('login/', supabase_login, name='login'),
    path('logout/', supabase_logout, name='logout'),
    # Redirección de la raíz
    path('', lambda request: redirect('admin_index', permanent=False)),
    path('registro/', supabase_register, name='supabase_register'),
    path('admin/usuarios/', admin_users, name='admin_users'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
