from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count, Avg, Q

from .models import Alumno, Materia, Calificacion
from .forms import AlumnoForm, MateriaForm, CalificacionForm

import openpyxl
from openpyxl import load_workbook

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib.auth.models import User
import random
import string
from django.db.models import Max

# ===============================
# 📊 DASHBOARD
# ===============================

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
def lista_alumnos(request):

    # 🔥 SI ES ALUMNO → SOLO VE UNO
    if hasattr(request.user, 'alumno'):
        alumnos = [request.user.alumno]
    else:
        alumnos = Alumno.objects.all()

    return render(request, 'alumnos/lista_alumnos.html', {
        'alumnos': alumnos
    })




def generar_matricula():
    ultimo = Alumno.objects.aggregate(Max('matricula'))['matricula__max']

    if ultimo:
        return int(ultimo) + 1
    return 1001



@login_required
@permission_required('alumnos.add_alumno', raise_exception=True)
@login_required
def crear_alumno(request):

    form = AlumnoForm(request.POST or None)

    if 'materias' in form.fields:
        form.fields['materias'].queryset = Materia.objects.all()

    if request.method == 'POST':
        if form.is_valid():

            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']

            # 🔥 MATRÍCULA AUTOMÁTICA
            matricula = generar_matricula()

            # 🔥 USERNAME = CORREO
            username = correo

            # 🔥 VALIDAR USUARIO DUPLICADO
            if User.objects.filter(username=username).exists():
                form.add_error('correo', 'Este correo ya tiene usuario')
            else:

                # 🔥 PASSWORD AUTOMÁTICO
                password = form.cleaned_data['password']

                # 🔥 CREAR USUARIO
                user = User.objects.create_user(
                    username=username,
                    email=correo,
                    password=password
                )

                # 🔥 CREAR ALUMNO
                alumno = form.save(commit=False)
                alumno.user = user
                alumno.matricula = matricula
                alumno.save()

                form.save_m2m()

                from django.contrib import messages
                messages.success(
                    request,
                    f"Usuario: {correo} | Contraseña: {password} | Matrícula: {matricula}"
                )

                return redirect('lista_alumnos')

    return render(request, 'alumnos/crear_alumno.html', {
        'form': form
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
            form.save()
            messages.success(request, 'Materia creada correctamente')
            return redirect('lista_materias')
    else:
        form = MateriaForm()

    return render(request, 'alumnos/crear_materia.html', {'form': form})


# ===============================
# 📊 DETALLE + CALIFICACIONES
# ===============================

@login_required
def detalle_alumno(request, id=None):

    # 🔥 SI ES ALUMNO → SOLO VE SU INFO
    if hasattr(request.user, 'alumno'):
        alumno = request.user.alumno

    else:
        alumno = Alumno.objects.get(id=id)

    calificaciones = Calificacion.objects.filter(alumno=alumno)

    promedio = calificaciones.aggregate(
        Avg('calificacion')
    )['calificacion__avg']

    return render(request, 'alumnos/detalle_alumno.html', {
        'alumno': alumno,
        'calificaciones': calificaciones,
        'promedio': promedio
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