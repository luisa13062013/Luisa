from django.db import models

# Create your models here.
class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    genero = models.CharField(max_length=100)
    paginas = models.IntegerField()
    fecha_de_publicacion = models.DateField()

    def __str__(self):
        return self.titulo