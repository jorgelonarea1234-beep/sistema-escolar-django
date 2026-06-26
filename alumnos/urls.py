from django.urls import path
from . import views


urlpatterns = [

    # 👨‍🎓 ALUMNOS
    path('', views.lista_alumnos, name='lista_alumnos'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('editar/<int:id>/', views.editar_alumno, name='editar_alumno'),
    path('eliminar/<int:id>/', views.eliminar_alumno, name='eliminar_alumno'),

    # 📊 DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
    

    # 📥📤 EXCEL
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('importar-excel/', views.importar_excel, name='importar_excel'),

    # 📚 MATERIAS
    path('materias/', views.lista_materias, name='lista_materias'),
    path('materias/crear/', views.crear_materia, name='crear_materia'),

    # 📊 DETALLE
    path('detalle/<int:id>/', views.detalle_alumno, name='detalle_alumno'),

    # 🧾 CALIFICACIONES
    path('calificaciones/crear/<int:alumno_id>/', views.crear_calificacion, name='crear_calificacion'),
    path('calificaciones/editar/<int:id>/', views.editar_calificacion, name='editar_calificacion'),
    path('calificaciones/eliminar/<int:id>/', views.eliminar_calificacion, name='eliminar_calificacion'),
    
    
    #REGULARIZACIONES
    path('regularizaciones/', views.lista_regularizaciones, name='lista_regularizaciones'),
    path('regularizaciones/<int:pk>/', views.capturar_regularizacion, name='capturar_regularizacion'),

    #KARDEX
    path('kardex/<int:id>/', views.kardex_alumno, name='kardex_alumno'),

    
    # ⚡ AJAX CALIFICACIONES
    path('calificaciones/crear_ajax/', views.crear_calificacion_ajax),
    path('calificaciones/editar_ajax/', views.editar_calificacion_ajax),
    path('calificaciones/eliminar_ajax/', views.eliminar_calificacion_ajax),

    # 📄 PDF
    path('boleta/pdf/<int:id>/', views.generar_pdf, name='generar_pdf'),

    # 🎓 CARRERAS
    path('carreras/', views.lista_carreras, name='lista_carreras'),
    path('carreras/crear/', views.crear_carrera, name='crear_carrera'),
    path('carreras/<int:carrera_id>/materias/', views.asignar_materias_carrera, name='asignar_materias_carrera'),

    # 👨‍🏫 MAESTROS
    path('maestros/', views.lista_maestros, name='lista_maestros'),
    path('maestros/crear/', views.crear_maestro, name='crear_maestro'),

    # 🔥 AGREGAR
    path('materias/editar/<int:id>/', views.editar_materia, name='editar_materia'),
    path('materias/eliminar/<int:id>/', views.eliminar_materia, name='eliminar_materia'),

    # 🔥 AGREGAR
    path('carreras/eliminar/<int:id>/', views.eliminar_carrera, name='eliminar_carrera'),

    path('carreras/editar/<int:id>/', views.editar_carrera, name='editar_carrera'),

    # ⚡ AJAX MAESTROS
    path('maestros/crear_ajax/', views.crear_maestro_ajax, name='crear_maestro_ajax'),
    path('maestros/editar_ajax/', views.editar_maestro_ajax, name='editar_maestro_ajax'),
    path('maestros/eliminar_ajax/', views.eliminar_maestro_ajax, name='eliminar_maestro_ajax'),

    path('carreras/eliminar_ajax/', views.eliminar_carrera_ajax),
    path('materias/eliminar_ajax/', views.eliminar_materia_ajax),

    path('inscripcion/', views.inscripcion_materias, name='inscripcion_materias'),
    path('inscribir_materia/', views.inscribir_materia),

    path('horario/', views.horario_alumno, name='horario_alumno'),
    path('horarios/eliminar/', views.eliminar_horario, name='eliminar_horario'),
    path('horarios/agregar/', views.agregar_horario, name='agregar_horario'),

    #calificaciones parciales
    path('calificaciones/guardar_parciales/', views.guardar_parciales, name='guardar_parciales'),
    path('calificaciones/eliminar_parciales/', views.eliminar_parciales, name='eliminar_parciales'),
]