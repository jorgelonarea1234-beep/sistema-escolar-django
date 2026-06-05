def roles_usuario(request):

    user = request.user

    if user.is_authenticated:
        return {
            'es_admin': user.is_superuser or user.groups.filter(name='admin').exists(),
            'es_maestro': user.groups.filter(name='maestro').exists(),
            'es_alumno': user.groups.filter(name='alumno').exists(),
        }

    return {}