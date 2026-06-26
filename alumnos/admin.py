from django.contrib import admin
from .models import Alumno, Materia, Carrera, Calificacion, Maestro, Horario
from .models import ConfiguracionParcial
from .models import ConfiguracionRegularizacion


admin.site.register(ConfiguracionParcial)
admin.site.register(ConfiguracionRegularizacion)

class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1

class MateriaAdmin(admin.ModelAdmin):
    inlines = [HorarioInline]

admin.site.register(Materia, MateriaAdmin)
admin.site.register(Horario)
admin.site.register(Maestro)
admin.site.register(Carrera)
admin.site.register(Alumno)
admin.site.register(Calificacion)
