from django.db import models

class DocumentoPDF(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='pdfs/')
    etiquetas = models.CharField(max_length=255, blank=True)  # Opcional: para almacenar etiquetas en texto
    fecha_creacion = models.DateTimeField(auto_now_add=True)


    def __str__(self):
      return self.nombre
