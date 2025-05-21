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


class SupabaseUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_class = models.CharField(max_length=255, db_column='class')  # "class" es palabra reservada
    email = models.CharField(max_length=255, null=True, db_column='email')

    class Meta:
        db_table = 'users'
        managed = False  # Importante: no dejar que Django cree/modifique esta tabla
    
class Plantilla(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    contenido_html = models.TextField()

