from django.db import models

class Boletin(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=False)  # Si False, es un borrador

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
