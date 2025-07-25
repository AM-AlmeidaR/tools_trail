"""
URL configuration for tools_control project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from tools_control import views
from tools_control.views import home_view, asignar_herramienta, devolver_herramienta, herramientas_disponibles, herramientas_asignadas, historial

urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('herramienta/asignar/', views.asignar_herramienta, name='asignar_herramienta'),
    path('herramienta/devolver/<int:herramienta_id>/', views.devolver_herramienta, name='devolver_herramienta'),
    path('herramientas/asignadas/', herramientas_asignadas, name='herramientas_asignadas'),
    path('herramientas/disponibles/', herramientas_disponibles, name='herramientas_disponibles'),
    path('historial/', historial, name='historial'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
