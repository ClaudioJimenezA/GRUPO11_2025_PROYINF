from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_boletines, name='lista_boletines'),
    path('nuevo/', views.boletin_form, name='nuevo_boletin'),
    path('boletin/<int:pk>/editar/', views.boletin_form, name='editar_boletin'),
    path('boletin/<int:pk>/preview/', views.preview_boletin, name='preview_boletin'),
    path('upload_image/', views.upload_image, name='upload_image'),

]

