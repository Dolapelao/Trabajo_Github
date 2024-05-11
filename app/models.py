from django.db import models

# Create your models here.

class Ejemplo(models.Model):
    hola = models.CharField(max_length=250, null=False)