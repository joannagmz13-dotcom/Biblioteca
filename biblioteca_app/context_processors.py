from .models import Alumno

def alumno_actual(request):
    alumno = None

    alumno_id = request.session.get('alumno_id')
    if alumno_id:
        try:
            alumno = Alumno.objects.get(id_alumno=alumno_id)
        except Alumno.DoesNotExist:
            pass

    return {
        'alumno': alumno
    }
