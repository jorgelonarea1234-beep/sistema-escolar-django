def roles_usuario(request):
    user = request.user

    return {
        'es_admin': user.is_authenticated and (
            user.is_superuser or user.groups.filter(name='ADMIN').exists()
        ),
        'es_maestro': user.is_authenticated and user.groups.filter(name='MAESTRO').exists(),
        'es_alumno': user.is_authenticated and user.groups.filter(name='ALUMNO').exists(),
    }