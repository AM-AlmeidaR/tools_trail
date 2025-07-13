from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from tools_trail.models import Operario, Herramienta, Registro
from django.utils import timezone
from django.utils.timezone import now
from django.http import HttpResponse
from django.core.files.base import ContentFile
import base64

def home_view(request):
    return render(request, 'home.html')
'''
def asignar_herramienta(request):
    if request.method == 'POST':
        codigo_herramienta = request.POST.get('codigo_herramienta')
        operario_id = request.POST.get('operario_id')
        firma_data = request.POST['firma']
        
        # Verificar que la herramienta existe
        herramienta = Herramienta.objects.filter(codigo=codigo_herramienta).first()
        if not herramienta:
            messages.error(request, f"La herramienta con código {codigo_herramienta} no existe.")
            return render(request, 'asignar_herramienta.html', {'operarios': Operario.objects.all()})
        
        # Verificar si está disponible
        if not herramienta.disponible:
            registro = Registro.objects.filter(herramienta=herramienta, fecha_devolucion__isnull=True).first()
            if registro:
                messages.error(request, f"La herramienta seleccionada no está disponible, la tiene asignada el operario nº {registro.operario.codigo}.")
            else:
                messages.error(request, "La herramienta seleccionada no está disponible.")
            return render(request, 'asignar_herramienta.html', {'operarios': Operario.objects.all()})
        
        # Verificar que el operario existe
        operario = Operario.objects.filter(id=operario_id).first()
        if not operario:
            messages.error(request, "El operario seleccionado no existe.")
            return render(request, 'asignar_herramienta.html', {'operarios': Operario.objects.all()})

        # Asignar herramienta
        herramienta.disponible = False
        herramienta.save()
        Registro.objects.create(herramienta=herramienta, operario=operario, fecha_asignacion=timezone.now())
        messages.success(request, f"La herramienta {codigo_herramienta} {herramienta.tipo} ha sido asignada al operario {operario.codigo} {operario.nombre} {operario.apellido}.")
    
    return render(request, 'asignar_herramienta.html', {'operarios': Operario.objects.all()})

'''

# función para validar la asignación de la herramienta con FIRMA

def asignar_herramienta(request):
    if request.method == "POST":
        herramienta_codigo = request.POST.get("codigo_herramienta")
        operario_id = request.POST.get("operario_id")
        signature_data = request.POST.get("signature_data")

        herramienta = get_object_or_404(Herramienta, codigo=herramienta_codigo)
        operario = get_object_or_404(Operario, id=operario_id)

        # Verificar si la herramienta está disponible
        if not herramienta.disponible:
            registro_existente = Registro.objects.filter(herramienta=herramienta, fecha_devolucion__isnull=True).first()
            if registro_existente:
                messages.error(request, f"La herramienta {herramienta.codigo} no está disponible, está asignada al operario nº {registro_existente.operario.codigo}.")
            else:
                messages.error(request, f"La herramienta {herramienta.codigo} no está disponible.")
            return redirect("asignar_herramienta")

         # Verificar si se ha proporcionado una firma válida
        if not signature_data or ';base64,' not in signature_data:
            messages.error(request, "La firma del operario es obligatoria para asignar la herramienta.")
            return redirect("asignar_herramienta")

        try:
            format, imgstr = signature_data.split(';base64,')
            ext = format.split('/')[-1]
            signature_file = ContentFile(base64.b64decode(imgstr), name=f"firma_{operario.codigo}.{ext}")
        except ValueError:
            messages.error(request, "La firma proporcionada no es válida.")
            return redirect("asignar_herramienta")
        
        herramienta.disponible = False
        herramienta.save()



        # Marcar la herramienta como no disponible

        # Crear registro de asignación
        Registro.objects.create(
            herramienta=herramienta,
            operario=operario,
            fecha_asignacion=timezone.now(),
            firma=signature_file
        )

        messages.success(request, f"La herramienta {herramienta.codigo} ha sido asignada al operario {operario.nombre} {operario.apellido}.")
        return redirect("herramientas_disponibles")

    operarios = Operario.objects.all()
    return render(request, "asignar_herramienta.html", {"operarios": operarios})

        # Asignar firma predeterminada si no hay una firma
'''        if not signature_data or ';base64,' not in signature_data:
            with open('static/images/firma_default.png', 'rb') as f:
                signature_file = ContentFile(f.read(), name=f"firma_{operario.codigo}_default.png")
        else:
            try:
                format, imgstr = signature_data.split(';base64,')
                ext = format.split('/')[-1]
                signature_file = ContentFile(base64.b64decode(imgstr), name=f"firma_{operario.codigo}.{ext}")
            except ValueError:
                messages.error(request, "La firma proporcionada no es válida.")
                return redirect("asignar_herramienta")
'''


def devolver_herramienta(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, id=herramienta_id)

    # Buscar el registro activo de asignación
    registro = Registro.objects.filter(herramienta=herramienta, fecha_devolucion__isnull=True).first()

    if registro:
        # Actualizar la fecha de devolución en el registro
        registro.fecha_devolucion = timezone.now()
        registro.save()

        # Marcar la herramienta como disponible
        herramienta.disponible = True
        herramienta.save()

        messages.success(request, f"La herramienta {herramienta.tipo} vuelve a estar disponible.")
    else:
        messages.error(request, "No se encontró un registro activo para esta herramienta.")

    return redirect("herramientas_asignadas")


def herramientas_disponibles(request):
    herramientas = Herramienta.objects.filter(disponible=True)
    return render(request, 'herramientas_disponibles.html', {'herramientas': herramientas})

def herramientas_asignadas(request):
    registros = Registro.objects.filter(fecha_devolucion__isnull=True).select_related('herramienta', 'operario')
    return render(request, 'herramientas_asignadas.html', {'registros': registros})

def historial(request):
    registros = Registro.objects.all()
    return render(request, "historial.html", {"registros": registros})
