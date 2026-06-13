from django import forms
from .models import Alumno
from .models import Materia
from django.contrib.auth.models import User
from .models import Calificacion
from .models import Maestro
from django import forms


class MaestroForm(forms.ModelForm):

    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Correo"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )

    class Meta:
        model = Maestro
        fields = ['nombre']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
 

class MateriaForm(forms.ModelForm):
    class Meta:

        model = Materia
        fields = ['nombre', 'clave', 'carreras', 'maestro']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'clave': forms.TextInput(attrs={'class': 'form-control'}),

            'carreras': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'maestro': forms.Select(attrs={'class': 'form-control'}),

            # 🔥 NUEVOS (CLAVE)
            #'dia': forms.Select(attrs={'class': 'form-control'}),

            #'hora_inicio': forms.TimeInput(
            #    attrs={'class': 'form-control', 'type': 'time'}
            #),

            #'hora_fin': forms.TimeInput(
            #    attrs={'class': 'form-control', 'type': 'time'}
            #),
        }




class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['materia', 'calificacion']
        widgets = {
            'materia': forms.Select(attrs={
                'class': 'form-control'
            }),
            'calificacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100
            }),
        }


from django import forms
from .models import Alumno

class AlumnoForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña",
        required=False  # 🔥 importante para editar
    )

    class Meta:
        model = Alumno
        fields = ['nombre', 'correo', 'carrera']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'carrera': forms.Select(attrs={'class': 'form-control'}),
        }

    # 🔥 LIMPIEZA CORRECTA (SIN ROMPER CARRERA)
    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get('nombre')
        if nombre:
            cleaned_data['nombre'] = nombre.upper()

        return cleaned_data

    # 🔥 VALIDAR CORREO ÚNICO
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')

        if Alumno.objects.filter(correo=correo).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Este correo ya está registrado")

        return correo