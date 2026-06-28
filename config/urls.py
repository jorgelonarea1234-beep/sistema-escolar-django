from django.contrib import admin
from django.urls import path, include
from alumnos.views import login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('', login_view, name='login'),

    path('admin/', admin.site.urls),

    path('alumnos/', include('alumnos.urls')),

    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)