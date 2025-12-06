from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Ejemplar
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
# --- Django: Autenticación ---
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


@login_required()
def home(request):
    return render(request, 'dashboard.html')


def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('home')
        else:
            form.errors.pop('__all__', None)  # Remueve el mensaje de Django
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect("login")


##alumno
from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno
from .forms import AlumnoForm


# LISTAR
@login_required()
def alumno_list(request):
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/list.html', {'alumnos': alumnos})


# CREAR
@login_required()
def alumno_create(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alumno_list')
    else:
        form = AlumnoForm()
    return render(request, 'alumnos/form.html', {'form': form, 'titulo': 'Agregar Alumno'})


# EDITAR
@login_required()
def alumno_update(request, id):
    alumno = get_object_or_404(Alumno, pk=id)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('alumno_list')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'alumnos/form.html', {'form': form, 'titulo': 'Editar Alumno'})


# ELIMINAR

@login_required()
def alumno_delete(request, id):
    alumno = get_object_or_404(Alumno, pk=id)
    alumno.delete()
    return redirect('alumno_list')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria
from .forms import CategoriaForm


# LISTAR
@login_required()
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/list.html', {'categorias': categorias})


# CREAR@
# login_required()
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/form.html', {'form': form, 'titulo': 'Agregar Categoría'})


# EDITAR
@login_required()
def categoria_update(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/form.html', {'form': form, 'titulo': 'Editar Categoría'})


# ELIMINAR
@login_required()
def categoria_delete(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    categoria.delete()
    return redirect('categoria_list')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor
from .forms import AutorForm


# LISTA
@login_required()
def autor_list(request):
    autores = Autor.objects.all()
    return render(request, 'autores/list.html', {'autores': autores})


# CREAR
@login_required()
def autor_create(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('autor_list')
    else:
        form = AutorForm()
    return render(request, 'autores/form.html', {'form': form, 'titulo': 'Agregar Autor'})


# EDITAR
@login_required()
def autor_update(request, id):
    autor = get_object_or_404(Autor, pk=id)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('autor_list')
    else:
        form = AutorForm(instance=autor)
    return render(request, 'autores/form.html', {'form': form, 'titulo': 'Editar Autor'})


# ELIMINAR
@login_required()
def autor_delete(request, id):
    autor = get_object_or_404(Autor, pk=id)
    autor.delete()
    return redirect('autor_list')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro, LibroAutor
from .forms import LibroForm


# LISTA
@login_required()
def libro_list(request):
    libros = Libro.objects.all()
    return render(request, "libros/lista.html", {"libros": libros})


# CREAR
@login_required()
def libro_create(request):
    if request.method == "POST":
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.save()

            # Guardar autores
            libro.autores.set(form.cleaned_data['autores'])

            # Crear ejemplares automáticamente
            cantidad = libro.cantidad_disponible
            for i in range(1, cantidad + 1):
                Ejemplar.objects.create(
                    libro=libro,
                    num_ejemplar=i,
                    estado_ejemplar='disponible'
                )

            return redirect("libro_list")
    else:
        form = LibroForm()

    return render(request, "libros/form.html", {"form": form, "titulo": "Nuevo Libro"})


# EDITAR
@login_required()
def libro_update(request, id):
    libro = get_object_or_404(Libro, id_libro=id)

    # Guardamos la cantidad original ANTES de cargar el form
    cantidad_original = libro.cantidad_disponible

    form = LibroForm(request.POST or None, request.FILES or None, instance=libro)

    if request.method == "POST" and form.is_valid():
        libro = form.save(commit=False)
        libro.save()

        libro.autores.set(form.cleaned_data['autores'])

        cantidad_nueva = libro.cantidad_disponible

        if cantidad_nueva > cantidad_original:
            inicio = cantidad_original + 1
            fin = cantidad_nueva + 1
            for i in range(inicio, fin):
                Ejemplar.objects.create(
                    libro=libro,
                    num_ejemplar=i,
                    estado_ejemplar="disponible"
                )

        # -------------------------
        # ELIMINAR ejemplares sobrantes si disminuye
        # -------------------------
        elif cantidad_nueva < cantidad_original:
            Ejemplar.objects.filter(
                libro=libro,
                num_ejemplar__gt=cantidad_nueva
            ).delete()

        return redirect("libro_list")

    return render(request, "libros/form.html", {"form": form, "titulo": "Editar Libro"})


# ELIMINAR (SweetAlert2)
@login_required()
def libro_delete(request, id):
    libro = get_object_or_404(Libro, id_libro=id)
    libro.delete()
    return redirect("libro_list")


from django.shortcuts import render, redirect
from .models import Alumno, Libro, Ejemplar, Prestamo
from datetime import date


@login_required()
def prestamo_create(request):
    alumnos = Alumno.objects.filter(estado='activo')
    libros = Libro.objects.all()

    if request.method == "POST":
        alumno_id = request.POST["alumno"]
        ejemplar_id = request.POST["ejemplar"]
        fecha_prestamo = request.POST["fecha_prestamo"]
        fecha_vencimiento = request.POST["fecha_vencimiento"]

        Prestamo.objects.create(
            alumno_id=alumno_id,
            ejemplar_id=ejemplar_id,
            fecha_prestamo=fecha_prestamo,
            fecha_vencimiento=fecha_vencimiento,
            estado="activo"
        )

        # Marcar ejemplar como prestado
        ej = Ejemplar.objects.get(id_ejemplar=ejemplar_id)
        ej.estado_ejemplar = "prestado"
        ej.save()

        return redirect("prestamo_list")

    return render(request, "prestamos/prestamo_form.html", {
        "alumnos": alumnos,
        "libros": libros
    })


from django.http import JsonResponse
from .models import Ejemplar


@login_required()
def ejemplares_disponibles(request, libro_id):
    ejemplares = Ejemplar.objects.filter(
        libro_id=libro_id,
        estado_ejemplar="disponible"
    )

    data = [
        {"id": e.id_ejemplar, "num": e.num_ejemplar, "estado": e.estado_ejemplar}
        for e in ejemplares
    ]

    return JsonResponse(data, safe=False)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Prestamo, Ejemplar, Devolucion
from datetime import date

from django.db.models import Count
from datetime import date


@login_required()
def prestamo_list(request):
    prestamos = (
        Prestamo.objects
        .select_related("alumno", "ejemplar")
        .annotate(num_multas=Count("multa"))
        .order_by('-id_prestamo')
    )

    hoy = date.today()

    # Actualizar estado según fechas
    for p in prestamos:
        if p.estado == "activo" and p.fecha_vencimiento < hoy:
            p.estado = "retrasado"
            p.save()

    return render(request, "prestamos/prestamo_list.html", {
        "prestamos": prestamos
    })


@login_required()
def prestamo_devolver(request, id):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id)
    ejemplar = prestamo.ejemplar

    hoy = date.today()

    # Verificar si hay retraso
    if hoy > prestamo.fecha_vencimiento:
        return JsonResponse({"retraso": True})

    # Si no hay retraso → devolver
    Devolucion.objects.create(
        prestamo=prestamo,
        fecha_entrega=hoy,
        observaciones="Devuelto sin observaciones"
    )

    prestamo.estado = "devuelto"
    prestamo.save()

    ejemplar.estado_ejemplar = "disponible"
    ejemplar.save()

    return JsonResponse({"retraso": False})


from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Prestamo, Devolucion, Multa, Ejemplar


# ----------------------------
# MULTA AUTOMÁTICA
# ----------------------------
@login_required()
def multa_automatica(request, id):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id)
    ejemplar = prestamo.ejemplar

    hoy = date.today()
    dias_retraso = (hoy - prestamo.fecha_vencimiento).days

    # Validación
    if dias_retraso <= 0:
        return JsonResponse({"ok": False, "msg": "No tiene retraso."})

    monto_sugerido = dias_retraso * 10  # 10 por día

    # Si el usuario está enviando el formulario
    if request.method == "POST":
        monto = request.POST.get("monto")
        motivo = f"Devolución tardía ({dias_retraso} días)"

        # Crear multa
        Multa.objects.create(
            prestamo=prestamo,
            monto=monto,
            motivo=motivo
        )

        # Registrar devolución
        Devolucion.objects.create(
            prestamo=prestamo,
            fecha_entrega=hoy,
            observaciones="Devuelto con multa automática"
        )

        # Cambiar estado del prestamo
        prestamo.estado = "devuelto"
        prestamo.save()

        # Actualizar estado del ejemplar
        ejemplar.estado_ejemplar = "disponible"
        ejemplar.save()

        return JsonResponse({"ok": True})

    # Respuesta al abrir modal
    return JsonResponse({
        "ok": True,
        "dias": dias_retraso,
        "monto": monto_sugerido
    })


import json


@login_required()
def multa_manual(request, id):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id)
    ejemplar = prestamo.ejemplar

    if request.method == "POST":

        data = json.loads(request.body.decode("utf-8"))

        monto = data.get("monto")
        motivo = data.get("motivo")
        danado = data.get("danado")

        # Validación
        if monto in [None, ""]:
            return JsonResponse({"ok": False, "msg": "El monto no puede estar vacío."})

        Multa.objects.create(
            prestamo=prestamo,
            monto=monto,
            motivo=motivo
        )

        if danado:
            ejemplar.estado_ejemplar = "dañado"
            ejemplar.save()

        return JsonResponse({"ok": True})

    return JsonResponse({"ok": False, "msg": "Método no permitido"})


@login_required()
def prestamo_devolver_sin_multa(request, id):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id)
    ejemplar = prestamo.ejemplar

    hoy = date.today()

    # Registrar devolución SIN MULTA
    Devolucion.objects.create(
        prestamo=prestamo,
        fecha_entrega=hoy,
        observaciones="Devuelto sin multa"
    )

    prestamo.estado = "devuelto"
    prestamo.save()

    ejemplar.estado_ejemplar = "disponible"
    ejemplar.save()

    return JsonResponse({"ok": True})


@login_required()
def ver_multas_prestamo(request, id_prestamo):
    try:
        prestamo = Prestamo.objects.get(pk=id_prestamo)
    except Prestamo.DoesNotExist:
        return JsonResponse({"ok": False})

    multas = prestamo.multa_set.all().values("monto", "motivo")

    return JsonResponse({
        "ok": True,
        "multas": list(multas)
    })


@login_required()
def prestamo_multas(request, id):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id)
    multas = Multa.objects.filter(prestamo=prestamo)

    return render(request, "multas/multas_list.html", {
        "prestamo": prestamo,
        "multas": multas
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Alumno
from .forms import LoginAlumnoForm


def login_alumno(request):
    if request.method == "POST":
        form = LoginAlumnoForm(request.POST)

        if form.is_valid():
            matricula = form.cleaned_data['matricula']

            try:
                alumno = Alumno.objects.get(matricula=matricula)

                if alumno.estado != "activo":
                    messages.error(request, "Tu cuenta está inactiva.")
                    return redirect('login_alumno')

                # Guardamos el alumno en sesión
                request.session['alumno_id'] = alumno.id_alumno

                return redirect('alumno_dashboard')

            except Alumno.DoesNotExist:
                messages.error(request, "La matrícula no existe.")
    else:
        form = LoginAlumnoForm()

    return render(request, "alumnos/login_alumno.html", {"form": form})


def alumno_dashboard(request):
    alumno_id = request.session.get('alumno_id')

    if not alumno_id:
        return redirect("login_alumno")

    alumno = get_object_or_404(Alumno, id_alumno=alumno_id)

    # ---- PRESTAMOS DEL ALUMNO ----
    prestamos = Prestamo.objects.filter(
        alumno=alumno,
        estado__in=["activo", "retrasado"]
    ).select_related(
        "ejemplar__libro"
    ).order_by('-fecha_prestamo')

    # ---- MULTAS ----
    multas = Multa.objects.filter(
        prestamo__alumno=alumno
    ).select_related("prestamo").order_by('-fecha')

    # Calcular total de multas
    multas_total = sum(m.monto for m in multas) if multas else 0

    return render(request, "alumnos/alumno_dashboard.html", {
        "alumno": alumno,
        "prestamos": prestamos,
        "multas": multas,
        "multas_total": multas_total,
    })


def logout_alumno(request):
    if "alumno_id" in request.session:
        del request.session["alumno_id"]

    return redirect("login_alumno")


from django.db.models import Q
def catalogo_libros(request):
    q = request.GET.get("q")
    disponible = request.GET.get("disponible")

    libros = Libro.objects.all().prefetch_related(
        "ejemplar_set", "autores", "categoria"
    )

    # 🔍 BUSCADOR
    if q:
        libros = libros.filter(
            Q(titulo__icontains=q) |
            Q(autores__nombre__icontains=q) |
            Q(categoria__nombre_categoria__icontains=q)
        ).distinct()

    # ✅ DISPONIBILIDAD
    for libro in libros:
        libro.disponible = libro.ejemplar_set.filter(
            estado_ejemplar="disponible"
        ).exists()

    if disponible == "true":
        libros = [l for l in libros if l.disponible]

    return render(request, "libros/catalogo.html", {
        "libros": libros
    })

def detalle_libro(request, id):
    libro = get_object_or_404(Libro, id_libro=id)
    ejemplares = libro.ejemplar_set.all()
    return render(request, "libros/detalle_libro.html", {"libro": libro, "ejemplares": ejemplares})