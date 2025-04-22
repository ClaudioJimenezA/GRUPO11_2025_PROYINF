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
    contenido = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'plugins': (
                    "advlist autolink lists link image charmap print preview anchor "
                    "searchreplace visualblocks code fullscreen "
                    "insertdatetime media table paste code help wordcount autosave"
                ),
                'toolbar': (
                    "undo redo | formatselect | bold italic backcolor | "
                    "alignleft aligncenter alignright alignjustify | "
                    "bullist numlist outdent indent | removeformat | help | "
                    "fullscreen | link image media | code"
                ),'style_formats': [
                    {'title': 'Título principal', 'block': 'h1'},
                    {'title': 'Subtítulo', 'block': 'h2'},
                    {'title': 'Párrafo normal', 'block': 'p'},
                    {'title': 'Cita', 'block': 'blockquote'},
                ],

                'autosave_interval': '10s',
                'autosave_retention': '2m',
                'menubar': True,
                'height': 600,
            }
        )
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    

    class Meta:
        model = Boletin
        fields = ['titulo', 'contenido']
