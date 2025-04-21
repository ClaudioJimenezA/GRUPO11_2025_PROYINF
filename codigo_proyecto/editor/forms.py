from django import forms
from .models import Boletin
from tinymce.widgets import TinyMCE
from django.db import models
from tinymce.models import HTMLField


class BoletinForm(forms.ModelForm):
    ESTADOS = (
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    )

    titulo = models.CharField(max_length=255)
    contenido = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    estado = models.CharField(max_length=10, choices=ESTADOS, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    

    class Meta:
        model = Boletin
        fields = ['titulo', 'contenido']
