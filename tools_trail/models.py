from django.db import models
from django.utils.timezone import now

class Operario(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.codigo})"
    
    class Meta:
        ordering = ['codigo']

class Herramienta(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=50, default= 'Generico')
    marca = models.CharField(max_length=50, default= 'Generico')
    modelo = models.CharField(max_length=50, default= 'Generico')
    numero_serie = models.CharField(max_length=50, unique=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo} - {self.codigo} ({'Disponible' if self.disponible else 'No Disponible'})"
    
    class Meta:
        ordering = ['tipo', 'codigo']

class Registro(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(default=now)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    firma = models.ImageField(upload_to='firmas/', null=True, blank=True)  # Nuevo campo para la firma

    def __str__(self):
        return f"Herramienta: {self.herramienta.tipo} {self.herramienta.codigo} asignada a {self.operario.codigo}"
    
    class Meta:
        ordering = ['herramienta']

