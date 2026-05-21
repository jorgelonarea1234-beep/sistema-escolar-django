from django.urls import path
from . import views

urlpatterns = [


    path('dashboard/',
      views.dashboard,
      name='dashboard'),

    path('', views.lista_alumnos, name='lista_alumnos'),

    path('crear/', views.crear_alumno, name='crear_alumno'),

    path('editar/<int:id>/',
         views.editar_alumno,
         name='editar_alumno'),

    path('eliminar/<int:id>/',
         views.eliminar_alumno,
         name='eliminar_alumno'),

    path(
    'exportar-excel/',
    views.exportar_excel,
    name='exportar_excel'),

    path(
    'importar-excel/',
    views.importar_excel,
    name='importar_excel'), 


    path('materias/', views.lista_materias, name='lista_materias'),
    path('materias/crear/', views.crear_materia, name='crear_materia'),   
    path('detalle/<int:id>/', views.detalle_alumno, name='detalle_alumno'), 
    path('calificaciones/crear/', views.crear_calificacion, name='crear_calificacion'),
    path('boleta/pdf/<int:id>/', views.generar_pdf, name='generar_pdf'),
    path('calificaciones/editar/<int:id>/', views.editar_calificacion, name='editar_calificacion'),
    path('calificaciones/eliminar/<int:id>/', views.eliminar_calificacion, name='eliminar_calificacion'),
]