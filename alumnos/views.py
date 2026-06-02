from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count, Avg, Q
from .models import Alumno, Materia, Calificacion
from .forms import AlumnoForm, MateriaForm, CalificacionForm
import openpyxl
from openpyxl import load_workbook
from .models import Carrera, Materia
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib.auth.models import User
import random
import string
from django.db.models import Max
from django.shortcuts import redirect
import json
from django.http import JsonResponse
from .models import Calificacion, Alumno, Materia
from .forms import MaestroForm
from .models import Maestro
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect


@login_required
def editar_carrera(request, id):

    carrera = get_object_or_404(Carrera, id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        print("NUEVO NOMBRE:", nombre)  # 🔥 DEBUG

        carrera.nombre = nombre
        carrera.save()

        return JsonResponse({'success': True})

    return render(request, 'alumnos/editar_carrera_modal.html', {
        'carrera': carrera
    })


def es_admin(user):
    return user.is_superuser

@user_passes_test(es_admin)
def eliminar_carrera(request, id):

    carrera = get_object_or_404(Carrera, id=id)
    carrera.delete()

    return redirect('lista_carreras')

@permission_required('alumnos.delete_materia', raise_exception=True)
def eliminar_materia(request, id):

    materia = get_object_or_404(Materia, id=id)
    materia.delete()

    return redirect('lista_materias')



@login_required
def editar_materia(request, id):

    materia = get_object_or_404(Materia, id=id)

    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})

    else:
        form = MateriaForm(instance=materia)

    return render(request, 'alumnos/editar_materia_modal.html', {
        'form': form,
        'materia': materia
    })




def login_view(request):

    print("ANTES:", request.user.is_authenticated)

    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        user = authenticate(request, username=correo, password=password)

        print("USER:", user)

        if user is not None:
            login(request, user)

            print("DESPUÉS:", request.user.is_authenticated)  # 🔥

            return redirect('/alumnos/')

    return render(request, 'registration/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')



def crear_maestro_ajax(request):
    import json
    from django.http import JsonResponse
    from .models import Maestro

    data = json.loads(request.body)

    Maestro.objects.create(nombre=data['nombre'])

    return JsonResponse({'status': 'ok'})




def editar_maestro_ajax(request):
    import json
    from django.http import JsonResponse
    from .models import Maestro

    data = json.loads(request.body)

    maestro = Maestro.objects.get(id=data['id'])
    maestro.nombre = data['nombre']
    maestro.save()

    return JsonResponse({'status': 'ok'})




def eliminar_maestro_ajax(request):
    import json
    from django.http import JsonResponse
    from .models import Maestro

    data = json.loads(request.body)
    Maestro.objects.get(id=data['id']).delete()
    return JsonResponse({'status': 'ok'})

def lista_maestros(request):

    maestros = Maestro.objects.all()

    return render(request, 'alumnos/lista_maestros.html', {
        'maestros': maestros
    })



def crear_maestro(request):

    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        # 🔥 VALIDAR CORREO
        if User.objects.filter(username=correo).exists():
            messages.error(request, "El correo ya está registrado")
            return render(request, 'alumnos/crear_maestro.html')

        # 🔥 CREAR USUARIO (CORREGIDO)
        user = User.objects.create_user(
            username=correo,
            email=correo,  # 👈🔥 IMPORTANTE
            password=password
        )

        Maestro.objects.create(user=user, nombre=nombre)

        messages.success(request, "Maestro creado correctamente")

        return redirect('lista_maestros')

    return render(request, 'alumnos/crear_maestro.html')





def crear_calificacion_ajax(request):
    import json
    from django.http import JsonResponse
    from .models import Calificacion, Alumno, Materia

    try:
        data = json.loads(request.body)

        print("DATA RECIBIDA:", data)

        alumno_id = data.get('alumno_id')
        materia_id = data.get('materia_id')
        calificacion_val = data.get('calificacion')

        if not alumno_id or not materia_id or not calificacion_val:
            return JsonResponse({
                'status': 'error',
                'mensaje': 'Datos incompletos'
            })

        try:
            calificacion = float(calificacion_val)
        except:
            return JsonResponse({
                'status': 'error',
                'mensaje': 'Calificación inválida'
            })

        if calificacion < 1 or calificacion > 100:
            return JsonResponse({
                'status': 'error',
                'mensaje': 'Calificación inválida (1-100)'
            })

        alumno = Alumno.objects.get(id=alumno_id)
        materia = Materia.objects.get(id=materia_id)

        calificacion_obj, created = Calificacion.objects.update_or_create(
            alumno=alumno,
            materia=materia,
            defaults={'calificacion': calificacion}
        )
        
        return JsonResponse({
            'status': 'ok',
            'id': calificacion_obj.id  # 🔥 ESTE ES EL ID REAL
        })

    except Exception as e:
        print("🔥 ERROR REAL:", str(e))
        return JsonResponse({
            'status': 'error',
            'mensaje': str(e)
        })



def guardar_calificacion_ajax(request):
    import json
    from django.http import JsonResponse
    from .models import Calificacion, Materia, Alumno

    data = json.loads(request.body)

    calificacion = int(data['calificacion'])

    # 🔥 VALIDACIÓN AQUÍ 👇
    if calificacion < 1 or calificacion > 100:
        return JsonResponse({
            'status': 'error',
            'mensaje': 'Calificación inválida (1-100)'
        })

    # 🔥 GUARDAR
    materia = Materia.objects.get(id=data['materia_id'])
    alumno = Alumno.objects.get(id=data['alumno_id'])

    Calificacion.objects.update_or_create(
        alumno=alumno,
        materia=materia,
        defaults={'calificacion': calificacion}
    )

    return JsonResponse({'status': 'ok'})






def editar_calificacion_ajax(request):
    import json
    from django.http import JsonResponse
    from .models import Calificacion

    data = json.loads(request.body)

    cal = Calificacion.objects.get(id=data['id'])

    # 🔥 VALIDACIÓN DE SEGURIDAD
    if hasattr(request.user, 'maestro'):
        if cal.materia.maestro != request.user.maestro:
            return JsonResponse({'error': 'No autorizado'}, status=403)

    # 🔥 ACTUALIZAR
    cal.calificacion = data['calificacion']
    cal.save()

    return JsonResponse({'status': 'ok'})


def eliminar_calificacion_ajax(request):
    import json
    from django.http import JsonResponse
    from .models import Calificacion

    data = json.loads(request.body)

    cal = Calificacion.objects.get(id=data['id'])
    cal.delete()

    return JsonResponse({'status': 'ok'})




@login_required
def dashboard(request):

    total_alumnos = Alumno.objects.count()

    total_carreras = Alumno.objects.values('carrera').distinct().count()

    carreras = Alumno.objects.values('carrera').annotate(total=Count('carrera'))

    labels = [c['carrera'] for c in carreras]
    data = [c['total'] for c in carreras]

    promedio_general = Calificacion.objects.aggregate(
        Avg('calificacion')
    )['calificacion__avg']

    return render(request, 'alumnos/dashboard.html', {
        'total_alumnos': total_alumnos,
        'total_carreras': total_carreras,
        'labels': labels,
        'data': data,
        'promedio_general': promedio_general,
    })


# ===============================
# 👨‍🎓 ALUMNOS
# ===============================
@login_required
def lista_carreras(request):
    carreras = Carrera.objects.all()

    return render(request, 'alumnos/lista_carreras.html', {
        'carreras': carreras
    })


@login_required
def lista_alumnos(request):

    user = request.user

    # 👑 ADMIN
    if user.is_superuser:
        alumnos = Alumno.objects.all()

    # 👨‍🏫 MAESTRO
    elif hasattr(user, 'maestro'):
        alumnos = Alumno.objects.filter(
            materias__maestro__user=user
        ).distinct()

    # 👨‍🎓 ALUMNO
    elif hasattr(user, 'alumno'):
        alumnos = Alumno.objects.filter(
            id=user.alumno.id
        )

    # 🔒 OTROS USUARIOS
    else:
        alumnos = Alumno.objects.none()

    return render(request, 'alumnos/lista_alumnos.html', {
        'alumnos': alumnos
    })



def crear_carrera(request):

    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        Carrera.objects.create(nombre=nombre.upper())

        return redirect('lista_carreras')

    return render(request, 'alumnos/crear_carrera.html')

def asignar_materias_carrera(request, carrera_id):

    carrera = get_object_or_404(Carrera, id=carrera_id)
    materias = Materia.objects.all()

    if request.method == 'POST':
        materias_ids = request.POST.getlist('materias')

        carrera.materia_set.set(materias_ids)  # 🔥 relación

        return redirect('lista_carreras')  # o donde quieras

    return render(request, 'alumnos/asignar_materias.html', {
        'carrera': carrera,
        'materias': materias,
        'materias_asignadas': carrera.materia_set.all()
    })


def generar_matricula(self):
    ultimo = Alumno.objects.exclude(matricula__isnull=True)\
                           .exclude(matricula__exact='')\
                           .order_by('-id')\
                           .first()
    
    if ultimo and '-' in ultimo.matricula:
        try:
            numero = int(ultimo.matricula.split('-')[-1]) + 1
        except:
            numero = 1
    else:
        numero = 1

    return f"ALU-{numero:04d}"



@login_required
@permission_required('alumnos.add_alumno', raise_exception=True)
def crear_alumno(request):

    carreras = Carrera.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        carrera_id = request.POST.get('carrera')

        # 🔥 validar usuario
        if User.objects.filter(username=correo).exists():
            messages.error(request, "El correo ya está registrado")
            return redirect('crear_alumno')

        # 🔥 crear usuario
        user = User.objects.create_user(
            username=correo,
            email=correo,
            password=password
        )

        # 🔥 obtener carrera
        carrera = Carrera.objects.get(id=carrera_id)

        # 🔥 crear alumno
        Alumno.objects.create(
            nombre=nombre,
            correo=correo,
            carrera=carrera,
            user=user
        )

        messages.success(request, "Alumno creado correctamente")
        return redirect('lista_alumnos')

    return render(request, 'alumnos/crear_alumno.html', {
        'carreras': carreras
    })






@login_required
@permission_required('alumnos.change_alumno', raise_exception=True)
def editar_alumno(request, id):

    alumno = Alumno.objects.get(id=id)

    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)

        if form.is_valid():
            form.save()

            messages.success(request, "Alumno actualizado correctamente")  # 🔥 AQUÍ

            return redirect('lista_alumnos')

    else:
        form = AlumnoForm(instance=alumno)

    return render(request, 'alumnos/editar_alumno.html', {
        'form': form
    })




@login_required
@permission_required('alumnos.delete_alumno', raise_exception=True)
def eliminar_alumno(request, id):

    alumno = Alumno.objects.get(id=id)
    alumno.delete()

    messages.success(request, 'Alumno eliminado correctamente')
    return redirect('lista_alumnos')


# ===============================
# 📚 MATERIAS
# ===============================

@login_required
def lista_materias(request):

    materias = Materia.objects.all()
    return render(request, 'alumnos/lista_materias.html', {'materias': materias})


@login_required
@permission_required('alumnos.add_materia', raise_exception=True)
def crear_materia(request):

    if request.method == 'POST':
        form = MateriaForm(request.POST)

        if form.is_valid():
            materia = form.save(commit=False)

            if hasattr(request.user, 'maestro'):
                materia.maestro = request.user.maestro

            materia.save()
            form.save_m2m()

            messages.success(request, 'Materia creada correctamente')
            return redirect('lista_materias')

    else:
        form = MateriaForm()  # 🔥 ESTA LÍNEA FALTABA

    return render(request, 'alumnos/crear_materia.html', {'form': form})

# ===============================
# 📊 DETALLE + CALIFICACIONES
# ===============================
@login_required
def detalle_alumno(request, id):

    alumno = Alumno.objects.get(id=id)

    # 🔥 MATERIAS SEGÚN SU CARRERA
    materias = Materia.objects.filter(
        carreras=alumno.carrera
    )

    calificaciones = Calificacion.objects.filter(
        alumno=alumno
    )

    return render(request, 'alumnos/detalle_alumno.html', {
        'alumno': alumno,
        'materias': materias,  # 🔥 IMPORTANTE
        'calificaciones': calificaciones
    })

  


# ===============================
# ➕ CALIFICACIONES
# ===============================

def crear_calificacion(request, alumno_id):

    alumno = Alumno.objects.get(id=alumno_id)

    # 🔥 AQUÍ VA
    print("MATERIAS DEL ALUMNO:", alumno.materias.all())


    form = CalificacionForm(request.POST or None)
    form.fields['materia'].queryset = alumno.materias.all()

    if request.method == 'POST':
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.alumno = alumno
            calificacion.save()
            return redirect('detalle_alumno', id=alumno.id)

    return render(request, 'alumnos/crear_calificacion.html', {
        'form': form,
        'alumno': alumno
    })


@login_required
@permission_required('alumnos.change_calificacion', raise_exception=True)
def editar_calificacion(request, id):

    calificacion = Calificacion.objects.get(id=id)

    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Calificación actualizada correctamente")
            return redirect('detalle_alumno', id=calificacion.alumno.id)
    else:
        form = CalificacionForm(instance=calificacion)

    return render(request, 'alumnos/crear_calificacion.html', {'form': form})


@login_required
@permission_required('alumnos.delete_calificacion', raise_exception=True)
def eliminar_calificacion(request, id):

    calificacion = Calificacion.objects.get(id=id)
    alumno_id = calificacion.alumno.id
    calificacion.delete()

    messages.success(request, "Calificación eliminada correctamente")

    return redirect('detalle_alumno', id=alumno_id)


# ===============================
# 📄 PDF
# ===============================

@login_required
def generar_pdf(request, id):

    alumno = Alumno.objects.get(id=id)
    calificaciones = Calificacion.objects.filter(alumno=alumno)
    promedio = calificaciones.aggregate(Avg('calificacion'))['calificacion__avg']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{alumno.nombre}.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(Paragraph(f"<b>Boleta de {alumno.nombre}</b>", styles['Title']))
    elementos.append(Paragraph(f"Matrícula: {alumno.matricula}", styles['Normal']))
    elementos.append(Paragraph(f"Carrera: {alumno.carrera}", styles['Normal']))
    elementos.append(Paragraph("<br/><br/>", styles['Normal']))

    data = [['Materia', 'Calificación']]
    for c in calificaciones:
        data.append([c.materia.nombre, str(c.calificacion)])

    table = Table(data)
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    elementos.append(table)

    if promedio:
        elementos.append(Paragraph(f"<b>Promedio: {round(promedio,2)}</b>", styles['Heading2']))

    doc.build(elementos)

    return response


# ===============================
# 📥📤 EXCEL
# ===============================

@login_required
def exportar_excel(request):

    workbook = openpyxl.Workbook()
    hoja = workbook.active
    hoja.title = 'Alumnos'

    hoja['A1'] = 'Matricula'
    hoja['B1'] = 'Nombre'
    hoja['C1'] = 'Correo'
    hoja['D1'] = 'Carrera'

    alumnos = Alumno.objects.all()

    fila = 2
    for alumno in alumnos:
        hoja[f'A{fila}'] = alumno.matricula
        hoja[f'B{fila}'] = alumno.nombre
        hoja[f'C{fila}'] = alumno.correo
        hoja[f'D{fila}'] = alumno.carrera
        fila += 1

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="alumnos.xlsx"'

    workbook.save(response)
    return response


@login_required
def importar_excel(request):

    if request.method == 'POST':

        archivo = request.FILES['archivo']
        workbook = load_workbook(archivo)
        hoja = workbook.active

        for fila in hoja.iter_rows(min_row=2):
            Alumno.objects.create(
                matricula=fila[0].value,
                nombre=fila[1].value,
                correo=fila[2].value,
                carrera=fila[3].value
            )

        messages.success(request, "Datos importados correctamente")
        return redirect('lista_alumnos')

    return render(request, 'alumnos/importar_excel.html')