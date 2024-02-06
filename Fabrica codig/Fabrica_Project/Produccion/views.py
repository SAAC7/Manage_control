from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import Orden_trabajo,Trabajo,Diseno_CNC,Trabajos_Orden
from Asesores.models import Presupuesto, Diseno
from Cotizadores.models import Cotizacion
from .models import Orden_trabajo

#Lista de ordenes de trabajo disponibles
@login_required(login_url='index')
def ordenes_listado(request):
    user = request.user
    if user.groups.filter(name='Asesor').exists():
        #pres = Presupuesto.objects.filter(fecha_fin=None, asesor=user).select_related('')
        #diseno = Diseno.objects.filter(presupuesto__in=pres, estado="Aprobado")
        #cotizacion = Cotizacion.objects.filter(diseno_id=diseno)
        #contrato = Orden_trabajo.objects.filter(presupuesto_id=pres)
        
        presupuesto_diseno = Presupuesto.objects.filter(fecha_fin=None, asesor=user,diseno__estado="Aprobado")
        ids_disenos = Presupuesto.objects.filter(fecha_fin=None, asesor=user, diseno__estado="Aprobado").values_list('diseno__id', flat=True)
        cotizacion = Cotizacion.objects.filter(diseno_id__in=ids_disenos).select_related('diseno')
        return render(request, 'Produccion/Ordenes_trabajo.html', {'presupuesto_diseno': presupuesto_diseno,'cotizaciones':cotizacion})
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        presupuesto_diseno = Presupuesto.objects.filter(fecha_fin=None, asesor=user,diseno__estado="Aprobado")
        ids_disenos = Presupuesto.objects.filter(fecha_fin=None, asesor=user, diseno__estado="Aprobado").values_list('diseno__id', flat=True)
        cotizacion = Cotizacion.objects.filter(diseno_id__in=ids_disenos).select_related('diseno')
        #cotizacion = Cotizacion.objects.filter(diseno_id=diseno)
        #contrato = Orden_trabajo.objects.filter(presupuesto_id=pres)
        return render(request, 'Produccion/Ordenes_trabajo.html', {'presupuesto_diseno': presupuesto_diseno, 'cotizaciones':cotizacion})
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
    

