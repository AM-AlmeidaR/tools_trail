from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Operario, Herramienta, Registro
from django.utils.timezone import now

def home_view(request):
    return render(request, 'home.html')

def asignar_herramienta(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, id=herramienta_id)
    
    if request.method == 'POST':
        operario_codigo = request.POST.get('operario_codigo')
        operario = get_object_or_404(Operario, codigo=operario_codigo)

        if herramienta.disponible:
            Registro.objects.create(operario=operario, herramienta=herramienta, fecha_asignacion=now())
            herramienta.disponible = False
            herramienta.save()
            messages.success(request, f"Herramienta {herramienta.codigo} asignada a {operario.codigo}")
        else:
            messages.error(request, f"La herramienta {herramienta.codigo} no está disponible.")

        return redirect('herramientas_disponibles')

    return render(request, 'asignar_herramienta.html', {'herramienta': herramienta})

def devolver_herramienta(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, id=herramienta_id)

    if not herramienta.disponible:
        registro = Registro.objects.filter(herramienta=herramienta, fecha_devolucion__isnull=True).first()
        if registro:
            registro.fecha_devolucion = now()
            registro.save()
            herramienta.disponible = True
            herramienta.save()
            messages.success(request, f"Herramienta {herramienta.codigo} devuelta correctamente.")
        else:
            messages.error(request, f"No se encontró un registro de asignación activo para {herramienta.codigo}.")
    else:
        messages.error(request, f"La herramienta {herramienta.codigo} ya está disponible.")

    return redirect('herramientas_asignadas')


def herramientas_disponibles(request):
    herramientas = Herramienta.objects.filter(disponible=True)
    return render(request, 'herramientas_disponibles.html', {'herramientas': herramientas})


def herramientas_asignadas(request):
    registros = Registro.objects.filter(fecha_devolucion__isnull=True).select_related('herramienta', 'operario')
    return render(request, 'herramientas_asignadas.html', {'registros': registros})
