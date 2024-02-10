from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse

#Modelos
from .models import Orden_trabajo,Trabajo,Diseno_CNC,Trabajos_Orden
from Asesores.models import Presupuesto, Diseno
from Cotizadores.models import Cotizacion



#Lista de ordenes de trabajo disponibles
@login_required(login_url='index')
def ordenes_listado(request):
    user = request.user
    lista_Ordenes=[]
    if user.groups.filter(name='Asesor').exists():
        ordenes = Orden_trabajo.objects.filter(presupuesto__asesor=user)
        for orden in ordenes:
        # Obtiene el diseño aprobado relacionado con la orden de trabajo, si existe
            diseno_aprobado = Diseno.objects.filter(presupuesto=orden.presupuesto, estado='Aprobado').first()       # Obtiene la cotización aprobada relacionada con el diseño, si existe
        if diseno_aprobado:
            cotizacion_aprobada = Cotizacion.objects.filter(diseno=diseno_aprobado, estado='Aprobado').first()
        else:
            cotizacion_aprobada = None          
        # Crea un diccionario con la información y lo añade a la lista de objetos
        objeto = {
            'orden': orden,
            'diseno_aprobado': diseno_aprobado,
            'cotizacion_aprobada': cotizacion_aprobada
        }
        lista_Ordenes.append(objeto)
        return render(
        request,
        'Produccion/Ordenes_trabajo.html',
        {'lista_Ordenes': lista_Ordenes}
        )
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        ordenes = Orden_trabajo.objects.all()
        for orden in ordenes:
        # Obtiene el diseño aprobado relacionado con la orden de trabajo, si existe
            diseno_aprobado = Diseno.objects.filter(presupuesto=orden.presupuesto, estado='Aprobado').first()       # Obtiene la cotización aprobada relacionada con el diseño, si existe
        if diseno_aprobado:
            cotizacion_aprobada = Cotizacion.objects.filter(diseno=diseno_aprobado, estado='Aprobado').first()
        else:
            cotizacion_aprobada = None          
        # Crea un diccionario con la información y lo añade a la lista de objetos
        objeto = {
            'orden': orden,
            'diseno_aprobado': diseno_aprobado,
            'cotizacion_aprobada': cotizacion_aprobada
        }
        lista_Ordenes.append(objeto)
        return render(
        request,
        'Produccion/Ordenes_trabajo.html',
        {'lista_Ordenes': lista_Ordenes}
        )
    
        
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
@login_required(login_url='index')        
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
@login_required(login_url='index')    
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
    
    
    
@login_required(login_url='index')    
def ordenes_info(request,or_id):
    user= request.user
    if (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        cotizacion = get_object_or_404(Cotizacion,pk=or_id)
        return render(request, 'Produccion/Ordenes_trabajo.html')
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})