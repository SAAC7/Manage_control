from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from Asesores.models import Presupuesto, Diseno
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .forms import DisenoForm
from django.http import HttpResponse
import datetime

# Create your views here.
@login_required(login_url='index')
def listadoP(request):
    user = request.user
    if user.groups.filter(name='Asesor').exists():
        pres = Presupuesto.objects.filter(fecha_fin=None, asesor=user, estado='Diseñando') 
        return render(request, 'Diseñador/listado_disenos_pendientes.html', {'pres': pres})
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        pres = Presupuesto.objects.filter(fecha_fin=None, estado='Diseñando') 
        return render(request, 'Diseñador/listado_disenos_pendientes.html', {'pres': pres})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
#Crear presupuesto
@login_required(login_url='index')
def nuevo_diseno(request, pre_id):
    user = request.user
    if (user.groups.filter(name='Asesor').exists() or user.groups.filter(name='Administrador').exists() or user.is_superuser):
        #form = DisenoForm()
        #return render(request, 'Diseñador/diseno.html', {'form': form})     
        # Obtener el presupuesto con el ID proporcionado
        presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
        return redirect('Designs/SubirArchivo', presupuesto)
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
#Redireccionar y obtener id del presupuesto
@login_required(login_url='index')
def obtener_presupuesto_id(request, pre_id):
    # Obtener el presupuesto con el ID proporcionado
    presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
    return redirect('/SubirArchivo/', presupuesto)