from django import template

register = template.Library()

@register.filter
def get_parcial(calificaciones, args):

    try:
        alumno_id, materia_id, parcial = str(args).split(',')
    except:
        return ''

    for c in calificaciones:
        if (
            str(c.alumno_id) == alumno_id and
            str(c.materia_id) == materia_id and
            str(c.parcial) == parcial
        ):
            return c.calificacion

    return ''


@register.filter
def get_promedio(calificaciones, args):

    try:
        alumno_id, materia_id = str(args).split(',')
    except:
        return '-'

    valores = [
        c.calificacion for c in calificaciones
        if str(c.alumno_id) == alumno_id and str(c.materia_id) == materia_id
    ]

    if valores:
        return round(sum(valores) / len(valores), 2)

    return '-'