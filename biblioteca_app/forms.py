from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Alumno

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['matricula', 'nombre', 'apellidos', 'semestre', 'grupo', 'estado']
        widgets = {
            'matricula': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }



#categorias

from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre_categoria']
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'form-control'}),
        }




from django import forms
from .models import Autor

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nacionalidad', 'nombre']
        widgets = {
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }



from django import forms
from .models import Libro, Autor

class LibroForm(forms.ModelForm):
    autores = forms.ModelMultipleChoiceField(
        queryset=Autor.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        required=True
    )

    class Meta:
        model = Libro
        fields = [
            'titulo',
            'editorial',
            'anio',
            'cantidad_disponible',
            'categoria',
            'autores',
            'imagen',
            'sinopsis',
        ]
        labels = {
            'anio': 'Año',
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'sinopsis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe aquí la sinopsis del libro...'
            }),
        }



class LoginAlumnoForm(forms.Form):
    matricula = forms.IntegerField(
        label="Matrícula",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu matrícula'
        })
    )