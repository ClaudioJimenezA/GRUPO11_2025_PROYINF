from django.db import models
from tinymce.models import HTMLField

class Boletin(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = HTMLField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
