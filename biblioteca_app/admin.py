from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Alumno, Rol, Categoria, Autor, Libro, LibroAutor,
    Ejemplar, Prestamo, Devolucion, Multa, Usuario
)



# ---------------------------
# usuarios
# ---------------------------
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Datos adicionales', {'fields': ('rol', 'alumno')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'rol',
                'alumno',
                'is_staff',
                'is_active'
            ),
        }),
    )

    list_display = ('username', 'first_name', 'last_name', 'email', 'rol', 'alumno', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')



# ---------------------------
# ALUMNOS
# ---------------------------
@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("id_alumno", "matricula", "nombre", "apellidos", "semestre", "grupo", "estado")
    search_fields = ("nombre", "apellidos", "matricula", "grupo")
    list_filter = ("estado", "semestre", "grupo")


# ---------------------------
# ROLES
# ---------------------------
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id_rol", "nombre_rol")
    search_fields = ("nombre_rol",)


# ---------------------------
# CATEGORIAS
# ---------------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id_categoria", "nombre_categoria")
    search_fields = ("nombre_categoria",)


# ---------------------------
# AUTORES
# ---------------------------
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("id_autor", "nombre", "nacionalidad")
    search_fields = ("nombre", "nacionalidad")


# ---------------------------
# LIBROS
# ---------------------------
class LibroAutorInline(admin.TabularInline):
    model = LibroAutor
    extra = 1


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("id_libro", "titulo", "editorial", "anio", "cantidad_disponible", "categoria")
    search_fields = ("titulo", "editorial")
    list_filter = ("categoria", "anio")
    inlines = [LibroAutorInline]


# ---------------------------
# EJEMPLARES
# ---------------------------
@admin.register(Ejemplar)
class EjemplarAdmin(admin.ModelAdmin):
    list_display = ("id_ejemplar", "libro", "num_ejemplar", "estado_ejemplar")
    list_filter = ("estado_ejemplar", "libro")
    search_fields = ("libro__titulo",)


# ---------------------------
# PRESTAMOS
# ---------------------------
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "id_prestamo", "alumno", "ejemplar",
        "fecha_prestamo", "fecha_vencimiento", "estado"
    )
    list_filter = ("estado", "fecha_prestamo", "fecha_vencimiento")
    search_fields = ("alumno__nombre", "alumno__apellidos")


# ---------------------------
# DEVOLUCIONES
# ---------------------------
@admin.register(Devolucion)
class DevolucionAdmin(admin.ModelAdmin):
    list_display = ("id_devolucion", "prestamo", "fecha_entrega", "observaciones")
    list_filter = ("fecha_entrega",)
    search_fields = ("prestamo__alumno__nombre", "observaciones")


# ---------------------------
# MULTAS
# ---------------------------
@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display = ("id_multa", "monto", "motivo", "prestamo")
    search_fields = ("motivo",)
    list_filter = ("monto",)
