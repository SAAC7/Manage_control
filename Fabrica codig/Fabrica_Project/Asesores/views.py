from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import Presupuesto, Diseno
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .forms import PresupuestoForm
from django.http import HttpResponse
import datetime

# Create your views here.
@login_required(login_url='index')
def listadoP(request):
    user = request.user
    if user.groups.filter(name='Asesor').exists():
        pres = Presupuesto.objects.filter(fecha_fin=None, asesor=user) 
        return render(request, 'Asesor/listado_presupuesto.html', {'pres': pres})
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        pres = Presupuesto.objects.filter(fecha_fin=None) 
        return render(request, 'Asesor/listado_presupuesto.html', {'pres': pres})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})

def presupuesto_list(request):
    #select_related es para hacer el JOIN y obtener los usuarios relacionados
    presupuestos = Presupuesto.objects.select_related('asesor').all()
    return render(request, )

def disenos_list(request):
    #select_related es para hacer el JOIN y obtener algunos datos del presupuesto
    disenos = Diseno.objects.select_related('usuario, presupuesto').all()
    
    #Iterando para obtener toda la informacion
    for diseno in disenos:
        print("Presupuesto ID:", presupuesto.id)
        print("Asesor Username:", presupuesto.asesor.username)
        print("Fecha Inicio:", presupuesto.fecha_inicio)
        print("Cliente:", presupuesto.cliente)
        print("Descripcion:", presupuesto.descripcion)
        print("Fecha Fin:", presupuesto.fecha_fin)
        print("\n")
        
    user = request.user
    if user.groups.filter(name='Asesor').exists():
        pres = Presupuesto.objects.filter(fecha_fin=None, asesor=user) 
        return render(request, 'Asesor/listado_presupuesto.html', {'pres': pres})
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        pres = Presupuesto.objects.filter(fecha_fin=None) 
        return render(request, 'Asesor/listado_presupuesto.html', {'pres': pres})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})

def listadoPF(request):
    user = request.user
    if user.groups.filter(name='Asesor').exists():
        pres = Presupuesto.objects.filter(fecha_fin__isnull=False, asesor=user) 
        return render(request, 'Asesor/listado_presupuesto_fin.html', {'pres': pres})
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        pres = Presupuesto.objects.filter(fecha_fin__isnull=False) 
        return render(request, 'Asesor/listado_presupuesto_fin.html', {'pres': pres})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})

@login_required(login_url='index')
def listadoD(request):
    user = request.user
    if user.groups.filter(name='Diseñador').exists():
        fordesign = Diseno.objects.filter(necesita_diseño=False) 
        return render(request,'Asesor/listado_presupuesto.html',{'fordesign':fordesign})

#Crear presupuesto
@login_required(login_url='index')
def presupuesto(request):
    user = request.user
    if (user.groups.filter(name='Asesor').exists() or user.groups.filter(name='Administrador').exists() or user.is_superuser):
        if request.method == 'POST':
            form = PresupuestoForm(request.POST, request.FILES)
            if form.is_valid():
                #obteniendo el valor del checkbox
                solicitud= form.cleaned_data['sol_design']
                
                #asignando estado segun el checkbox
                if solicitud:
                    estados = "Diseñando"
                else:
                    estados="Cotizando"
                    
                # Guardar el Presupuesto
                nombre_cliente = form.cleaned_data['nombre_cliente']
                descripcion = form.cleaned_data['descripcion']
                nuevo_presupuesto = Presupuesto.objects.create(cliente=nombre_cliente, descripcion=descripcion, asesor=user,estado=estados)

                # Guardar el Diseño
                archivo = form.cleaned_data['archivo']
                nuevo_diseno = Diseno.objects.create(usuario=request.user, presupuesto=nuevo_presupuesto, archivo=archivo)
                return redirect('/Presupuesto/')  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario
        else:
            form = PresupuestoForm()
            return render(request, 'Asesor/presupuesto.html', {'form': form}) 
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
    # Cambia 'nombre_del_template.html' por el nombre de tu template donde está el formulario

#Rechazar presupuesto
@login_required(login_url='index')
def presupuesto_rechazar(request, pre_id):
    # Obtener el presupuesto con el ID proporcionado
    presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
    # Actualizar el estado del presupuesto y la fecha de finalización
    presupuesto.estado = "Rechazado"
    presupuesto.fecha_fin = datetime.datetime.now()
    presupuesto.save()  # Guardar los cambios en la base de datos
    return redirect('/Presupuesto/')

#Mostrar diseños de presupuesto especificado
@login_required(login_url='index')
def disenos_presupuesto(request, pre_id):
    user = request.user
    if (user.groups.filter(name='Asesor').exists() or user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Designer').exists()):
        # Obtener el presupuesto con el ID proporcionado
        presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
        
        #Lista de diseños del presupuesto
        pres = Diseno.objects.filter(presupuesto_id=presupuesto)
        
        return render(request,'Designer/diseno.html', {'presupuesto':presupuesto, 'pres': pres})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    