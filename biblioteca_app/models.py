from django.db import models

from django.contrib.auth.models import AbstractUser

# ---------------------------
# ALUMNOS
# ---------------------------
class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True, db_column="IdAlumno")
    matricula = models.IntegerField(db_column="Matricula")
    nombre = models.CharField(max_length=30, db_column="Nombre")
    apellidos = models.CharField(max_length=30, db_column="Apellidos")
    semestre = models.IntegerField(db_column="Semestre")
    grupo = models.CharField(max_length=5, db_column="Grupo")
    estado = models.CharField(
        max_length=15,
        db_column="Estado",
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')]
    )

    class Meta:
        db_table = "alumnos"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

# ---------------------------
# ROLES
# ---------------------------
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True, db_column="IdRol")
    nombre_rol = models.CharField(max_length=20, db_column="NombreRol")

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.nombre_rol


# ---------------------------
# USUARIOS
# ---------------------------

class Usuario(AbstractUser):

    rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="IdRol"
    )

    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="IdAlumno"
    )

    def __str__(self):
        return self.first_name + " " + self.last_name


# ---------------------------
# CATEGORIAS
# ---------------------------
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True, db_column="IdCategoria")
    nombre_categoria = models.CharField(max_length=30, db_column="NombreCategoria")

    class Meta:
        db_table = "categorias"

    def __str__(self):
        return self.nombre_categoria


# ---------------------------
# AUTORES
# ---------------------------
class Autor(models.Model):
    id_autor = models.AutoField(primary_key=True, db_column="IdAutor")
    nacionalidad = models.CharField(max_length=30, db_column="Nacionalidad")
    nombre = models.CharField(max_length=30, db_column="Nombre")

    class Meta:
        db_table = "autores"

    def __str__(self):
        return self.nombre


# ---------------------------
# LIBROS
# ---------------------------
class Libro(models.Model):
    id_libro = models.AutoField(primary_key=True, db_column="IdLibro")
    titulo = models.CharField(max_length=30, db_column="Titulo")
    editorial = models.CharField(max_length=30, db_column="Editorial")
    anio = models.IntegerField(db_column="Anio")
    sinopsis = models.TextField(blank=True, null=True, db_column="Sinopsis")
    cantidad_disponible = models.IntegerField(db_column="CantidadDisponible")

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        db_column="IdCategoria"
    )

    autores = models.ManyToManyField(
        Autor,
        through="LibroAutor",
        related_name="libros"
    )
    imagen = models.ImageField(upload_to='libros/', blank=True, null=True) #Manejo de imagenes

    class Meta:
        db_table = "libros"

    def __str__(self):
        return self.titulo


# ---------------------------
# LIBRO - AUTOR (Tabla intermedia)
# ---------------------------
class LibroAutor(models.Model):
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        db_column="IdLibro"
    )
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        db_column="IdAutor"
    )

    class Meta:
        db_table = "libro_autor"
        unique_together = ("libro", "autor")


# ---------------------------
# EJEMPLARES
# ---------------------------
class Ejemplar(models.Model):
    id_ejemplar = models.AutoField(primary_key=True, db_column="IdEjemplar")
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        db_column="IdLibro"
    )
    num_ejemplar = models.IntegerField(db_column="NumEjemplar")
    estado_ejemplar = models.CharField(
        max_length=20,
        db_column="EstadoEjemplar",
        choices=[
            ('disponible', 'Disponible'),
            ('prestado', 'Prestado'),
            ('dañado', 'Dañado')
        ]
    )

    class Meta:
        db_table = "ejemplares"


# ---------------------------
# PRESTAMOS
# ---------------------------
class Prestamo(models.Model):
    id_prestamo = models.AutoField(primary_key=True, db_column="IdPrestamo")

    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.CASCADE,
        db_column="IdAlumno"
    )
    ejemplar = models.ForeignKey(
        Ejemplar,
        on_delete=models.CASCADE,
        db_column="IdEjemplar"
    )

    fecha_prestamo = models.DateField(db_column="FechaPrestamo")
    fecha_vencimiento = models.DateField(db_column="FechaVencimiento")

    estado = models.CharField(
        max_length=15,
        db_column="Estado",
        choices=[
            ('activo', 'Activo'),
            ('devuelto', 'Devuelto'),
            ('retrasado', 'Retrasado')
        ]
    )

    class Meta:
        db_table = "prestamos"


# ---------------------------
# DEVOLUCIONES
# ---------------------------
class Devolucion(models.Model):
    id_devolucion = models.AutoField(primary_key=True, db_column="IdDevolucion")
    fecha_entrega = models.DateField(db_column="FechaEntrega")
    observaciones = models.CharField(max_length=50, null=True, blank=True, db_column="Observaciones")

    prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE,
        db_column="IdPrestamo"
    )

    class Meta:
        db_table = "devoluciones"


# ---------------------------
# MULTAS
# ---------------------------
class Multa(models.Model):
    id_multa = models.AutoField(primary_key=True, db_column="IdMulta")
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column="Monto")
    motivo = models.CharField(max_length=30, null=True, blank=True, db_column="Motivo")
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, db_column="IdPrestamo")
    fecha = models.DateField(auto_now_add=True, db_column="Fecha")

    class Meta: db_table = "multas"
