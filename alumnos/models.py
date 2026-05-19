from django.db import models

class Alumno(models.Model):
    matricula = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200)
    correo = models.EmailField()
    carrera = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre