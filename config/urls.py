from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def inicio(request):
    return redirect('/alumnos/')

urlpatterns = [

    path('', inicio),  # 👈 ESTA LÍNEA FALTABA

    path('admin/', admin.site.urls),

    path('alumnos/', include('alumnos.urls')),

    path(
        'login/',
        auth_views.LoginView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
]