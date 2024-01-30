from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import Orden_trabajo,Trabajo,Diseno_CNC,Trabajos_Orden

def trabajo(request):
    usuario_autenticado = request.user
    
    if not usuario_autenticado.groups.filter(name__in=['Administrador', 'Superusuario', 'Designer', 'Asesor', 'Cotizador']).exists():
        trabajos = Trabajo.objects.filter(trabajador=usuario_autenticado,fecha_fin__isnull=True)
        return render(request, 'Produccion/trabajos.html', {'trabajos': trabajos})
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        trabajos = Trabajo.objects.filter(fecha_fin__isnull=True)
        return render(request, 'Produccion/trabajos.html', {'trabajos': trabajos})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
    
def trabajofin(request):
    usuario_autenticado = request.user
    if not usuario_autenticado.groups.filter(name__in=['Administrador', 'Designer', 'Asesor', 'Cotizador']).exists() or not user.is_superuser:
        trabajos = Trabajo.objects.filter(trabajador=usuario_autenticado,fecha_fin__isnull=False)
        return render(request, 'Produccion/trabajos_finalizados.html', {'trabajos': trabajos})
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        trabajos = Trabajo.objects.filter(fecha_fin__isnull=False)
        return render(request, 'Produccion/trabajos_finalizados.html', {'trabajos': trabajos})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    

