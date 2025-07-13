from django.contrib import admin

from django.contrib import admin
from .models import Operario, Herramienta, Registro

@admin.register(Operario)
class OperarioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'apellido')
    list_filter = ['codigo']
    search_fields = ['codigo']

@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'tipo', 'marca', 'modelo', 'numero_serie', 'disponible')
    list_filter = ('disponible', 'tipo',)

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('fecha_asignacion', 'operario', 'herramienta', 'fecha_devolucion')
    list_filter = ['fecha_asignacion', 'fecha_devolucion']

