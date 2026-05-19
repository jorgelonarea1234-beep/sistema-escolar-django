from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Alumno
from django.db.models import Count
from .forms import AlumnoForm
from django.http import HttpResponse
import openpyxl
from openpyxl import load_workbook
from django.contrib.auth.decorators import permission_required

@login_required
def dashboard(request):

    total_alumnos = Alumno.objects.count()

    total_carreras = Alumno.objects.values(
        'carrera'
    ).distinct().count()

    carreras = Alumno.objects.values(
        'carrera'
    ).annotate(
        total=Count('carrera')
    )

    labels = []
    data = []

    for carrera in carreras:

        labels.append(carrera['carrera'])

        data.append(carrera['total'])

    return render(
        request,
        'alumnos/dashboard.html',
        {

            'total_alumnos': total_alumnos,

            'total_carreras': total_carreras,

            'labels': labels,

            'data': data,
        }
    )


@login_required
def lista_alumnos(request):

    buscar = request.GET.get('buscar')

    if buscar:

        alumnos = Alumno.objects.filter(
            nombre__icontains=buscar
        )

    else:

        alumnos = Alumno.objects.all()

    return render(request, 'alumnos/lista_alumnos.html', {
        'alumnos': alumnos
    })

@login_required
@permission_required(
    'alumnos.change_alumno',
    raise_exception=True
)
def crear_alumno(request):

    if request.method == 'POST':

        form = AlumnoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
            request,
            'Alumno creado correctamente'
)
            return redirect('lista_alumnos')

    else:
        form = AlumnoForm()

    return render(request, 'alumnos/crear_alumno.html', {
        'form': form
    })
@login_required
@permission_required(
    'alumnos.change_alumno',
    raise_exception=True
)
def editar_alumno(request, id):

    alumno = Alumno.objects.get(id=id)

    if request.method == 'POST':

        form = AlumnoForm(request.POST, instance=alumno)

        if form.is_valid():
            form.save()
            messages.success(
            request,
            'Alumno actualizado correctamente'
)
            return redirect('lista_alumnos')

    else:
        form = AlumnoForm(instance=alumno)

    return render(request, 'alumnos/editar_alumno.html', {
        'form': form
    })

@login_required
@permission_required(
    'alumnos.delete_alumno',
    raise_exception=True
)

def eliminar_alumno(request, id):

    alumno = Alumno.objects.get(id=id)

    alumno.delete()
    messages.success(
    request,
    'Alumno eliminado correctamente'
)

    return redirect('lista_alumnos')



@login_required
def exportar_excel(request):

    workbook = openpyxl.Workbook()

    hoja = workbook.active

    hoja.title = 'Alumnos'

    # ENCABEZADOS

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

    response = HttpResponse(
        content_type=
        'application/ms-excel'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="alumnos.xlsx"'

    workbook.save(response)

    return response


@login_required
def importar_excel(request):

    if request.method == 'POST':

        archivo = request.FILES['archivo']

        workbook = load_workbook(archivo)

        hoja = workbook.active

        filas = hoja.iter_rows(min_row=2)

        importados = 0
        omitidos = 0

        for fila in filas:

            matricula = fila[0].value
            nombre = fila[1].value
            correo = fila[2].value
            carrera = fila[3].value

            # VALIDAR FILAS VACIAS

            if not matricula or not nombre:

                omitidos += 1
                continue

            # VALIDAR CORREO

            if not correo:

                omitidos += 1
                continue

            # VALIDAR DUPLICADOS

            existe = Alumno.objects.filter(
                matricula=matricula
            ).exists()

            if existe:

                omitidos += 1
                continue

            Alumno.objects.create(

                matricula=matricula,

                nombre=nombre,

                correo=correo,

                carrera=carrera,
            )

            importados += 1

        messages.success(

            request,

            f'''
            Importados: {importados}
            | Omitidos: {omitidos}
            '''
        )

        return redirect('lista_alumnos')

    return render(
        request,
        'alumnos/importar_excel.html'
    )