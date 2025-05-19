from django.db import models

class Boletin(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='boletines/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=False)  # Si False, es un borrador
    
    # Campo para distinguir plantilla de boletín común
    es_plantilla = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
