from django.contrib import admin
from .models import Alumno, Materia, Carrera, Calificacion


admin.site.register(Carrera)
admin.site.register(Alumno)
admin.site.register(Materia)
admin.site.register(Calificacion)
