from django.contrib import admin
from .models import Alumno
from .models import Materia

admin.site.register(Alumno)
admin.site.register(Materia)