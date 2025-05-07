
from django.db import models

class Conejo(models.Model):
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    edad = models.IntegerField()

