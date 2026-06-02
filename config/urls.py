from django.contrib import admin
from django.urls import path, include
from alumnos.views import login_view, logout_view

urlpatterns = [

    path('', login_view, name='login'),

    path('admin/', admin.site.urls),

    path('alumnos/', include('alumnos.urls')),

    path('logout/', logout_view, name='logout'),
]