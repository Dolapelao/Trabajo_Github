from django.db import models
from django.utils import timezone

# Create your models here.

class Actividade(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre

class Destino(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre
    
class Reserva(models.Model):
    nombre = models.CharField(max_length=50)
    actividad = models.ForeignKey(Actividade, on_delete=models.CASCADE)
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE)
    fecha_viaje = models.DateField()
    
    def __str__(self):
        return self.nombre
    
    @classmethod
    def reservas_este_mes(cls):
        hoy = timezone.now()
        return cls.objects.filter(fecha_viaje__year=hoy.year, fecha_viaje__month=hoy.month).count()

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=250)
    mensaje = models.TextField()
    
    def __str__(self):
        return self.nombre
