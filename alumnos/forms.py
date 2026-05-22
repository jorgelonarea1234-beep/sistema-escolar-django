from django import forms
from .models import Alumno
from .models import Materia
from django.contrib.auth.models import User
from .models import Calificacion


 

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

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )

    class Meta:
        model = Alumno
        fields = ['nombre', 'correo', 'carrera', 'materias']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control'}),
            'materias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        for campo in ['nombre', 'carrera']:
            valor = cleaned_data.get(campo)
            if valor:
                cleaned_data[campo] = valor.upper()

        return cleaned_data

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')

        if Alumno.objects.filter(correo=correo).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Este correo ya está registrado")

        return correo






    def clean(self):
        cleaned_data = super().clean()

        for campo in ['nombre', 'carrera']:
            valor = cleaned_data.get(campo)
            if valor:
                cleaned_data[campo] = valor.upper()

        return cleaned_data

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')

        if Alumno.objects.filter(correo=correo).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Este correo ya está registrado")

        return correo

    # 🔥 AQUÍ LA MAGIA
    def clean(self):
        cleaned_data = super().clean()

        for campo in ['nombre', 'carrera']:
            valor = cleaned_data.get(campo)
            if valor:
                cleaned_data[campo] = valor.upper()

        return cleaned_data

    # 🔥 VALIDACIÓN PERSONALIZADA
 