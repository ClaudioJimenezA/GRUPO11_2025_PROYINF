from django.db import models

class Boletin(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=False)  # Si False, es un borrador

    def __str__(self):
        return self.titulo
