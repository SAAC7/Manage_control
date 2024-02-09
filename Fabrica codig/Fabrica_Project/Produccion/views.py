from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse

#Modelos
from .models import Orden_trabajo,Trabajo,Diseno_CNC,Trabajos_Orden
from Asesores.models import Presupuesto, Diseno
from Cotizadores.models import Cotizacion
from .models import Orden_trabajo


#Lista de ordenes de trabajo disponibles
@login_required(login_url='index')
def ordenes_listado(request):
    user = request.user
    if user.groups.filter(name='Asesor').exists():
        presupuestos_aprobados = Presupuesto.objects.filter(
            asesor=user,
            diseno__estado="Aprobado",
            diseno__cotizacion__estado="Aprobado",
            orden_trabajo__isnull=False            
        ).distinct()

        return render(
            request,
            'Produccion/Ordenes_trabajo.html',
            {'presupuesto_diseno_cotizacion': presupuestos_aprobados}
        )
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        presupuestos_aprobados = Presupuesto.objects.filter(
            diseno__estado="Aprobado",
            diseno__cotizacion__estado="Aprobado",
            orden_trabajo__isnull=False 
        ).distinct()

        return render(
            request,
            'Produccion/Ordenes_trabajo.html',
            {'presupuesto_diseno_cotizacion': presupuestos_aprobados}
            )
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
        

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