from django import template

register = template.Library()

@register.filter
def get_calificacion(calificaciones, materia_id):
    return calificaciones.filter(materia_id=materia_id).first()