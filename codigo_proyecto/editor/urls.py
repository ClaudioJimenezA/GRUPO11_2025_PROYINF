from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_boletines, name='lista_boletines'),
    path('nuevo/', views.crear_boletin, name='nuevo_boletin'),
    path('preview/<int:pk>/', views.preview_boletin, name='preview_boletin'),
]
