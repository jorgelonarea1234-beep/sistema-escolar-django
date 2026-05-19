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
]