from django.db import models
from django.contrib.auth.models import User



class Maestro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre




class Carrera(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    clave = models.CharField(max_length=20)
    carreras = models.ManyToManyField(Carrera)
    maestro = models.ForeignKey(Maestro, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre
    


class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia, blank=True)

    matricula = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    def generar_matricula(self):

        ultimo = Alumno.objects.exclude(matricula__isnull=True)\
                               .exclude(matricula__exact='')\
                               .order_by('-matricula')\
                               .first()

        if ultimo:
            try:
                numero = int(ultimo.matricula.split('-')[-1]) + 1
            except:
                numero = 1
        else:
            numero = 1

        return f"ALU-{numero:04d}"

    def save(self, *args, **kwargs):
        if not self.matricula or self.matricula == '':
            self.matricula = self.generar_matricula()
        super().save(*args, **kwargs)



    
class Calificacion(models.Model):

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.alumno} - {self.materia} - {self.calificacion}"




