from django.db import models
from django.contrib.auth.models import User



class Materia(models.Model):

    nombre = models.CharField(max_length=100)
    clave = models.CharField(max_length=20)
    profesor = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre



class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    matricula = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    carrera = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    
class Calificacion(models.Model):

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    calificacion = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.alumno} - {self.materia} - {self.calificacion}"


