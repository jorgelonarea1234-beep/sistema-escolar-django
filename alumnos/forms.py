from django import forms
from .models import Alumno
from .models import Materia
from django.contrib.auth.models import User


 

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'profesor': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'clave': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }  


from .models import Calificacion

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





class AlumnoForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Alumno
        fields = ['matricula', 'nombre', 'correo', 'carrera']
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control'}),
        }