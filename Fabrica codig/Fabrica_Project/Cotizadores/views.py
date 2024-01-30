from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import datetime
from .models import *
from Asesores.models import Presupuesto, Diseno
# Create your views here.
@login_required(login_url='index')
def cotDisponibles(request):
    user = request.user
    
    if user.groups.filter(name='Cotizador').exists() or user.groups.filter(name='Administrador').exists() or user.is_superuser:
        # Obtener todos los presupuestos en estado 'cotizacion'
        presupuestos_cotizacion = Presupuesto.objects.filter(estado='Cotizando')

        # Crear una lista para almacenar la información de presupuestos y diseños asociados
        presupuestos_con_diseños = []

        # Iterar sobre cada presupuesto en estado de cotización
        for presupuesto in presupuestos_cotizacion:
            # Obtener el diseño asociado al presupuesto que no esté en estado de reserva
            diseño = Diseno.objects.filter(presupuesto=presupuesto, estado__exact='Cotizando').first()
        

        return render(request, 'Cotizador/listado.html', {'pres': presupuestos_con_diseños})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
   
@login_required(login_url='index')
def cotReservadas(request):
    return render(request, 'Cotizador/listado.html')

@login_required(login_url='index')
def cotFin(request):
    return render(request, 'Cotizador/listado.html')
