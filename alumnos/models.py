from django.db import models
from django.contrib.auth.models import User




class Carrera(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    profesor = models.CharField(max_length=100)
    clave = models.CharField(max_length=20)
    carreras = models.ManyToManyField(Carrera)  # 🔥 ahora sí funciona

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia, blank=True)  # opcional
    matricula = models.IntegerField(unique=True, null=True, blank=True)

    
class Calificacion(models.Model):

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.alumno} - {self.materia} - {self.calificacion}"




