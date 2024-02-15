from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
#Modelos
from .models import Presupuesto, Diseno
from Cotizadores.models import Cotizacion
from Produccion.models import Orden_trabajo
#Formularios
from .forms import PresupuestoForm
from .forms import ContratoForm


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

#Listado de presupuestos finalizados
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

#Listado de presupuestos que necesitan diseño
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
                    estado_di="Diseño guía"
                else:
                    estados="Cotizando"
                    estado_di="Aprobado"
                    
                # Guardar el Presupuesto
                nombre_cliente = form.cleaned_data['nombre_cliente']
                descripcion = form.cleaned_data['descripcion']
                nuevo_presupuesto = Presupuesto.objects.create(cliente=nombre_cliente, descripcion=descripcion, asesor=user,estado=estados)

                # Guardar el Diseño
                archivo = form.cleaned_data['archivo']
                nuevo_diseno = Diseno.objects.create(usuario=request.user, presupuesto=nuevo_presupuesto, archivo=archivo,estado=estado_di)
                return redirect('/Presupuesto/')  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario
        else:
            form = PresupuestoForm()
            return render(request, 'Asesor/presupuesto.html', {'form': form}) 
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
    # Cambia 'nombre_del_template.html' por el nombre de tu template donde está el formulario

#Subir contrato
@login_required(login_url='index')
def subir_contrato(request,id_p):
    user = request.user
    if (user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Cotizador').exists()):
        if request.method == 'POST':
            form = ContratoForm(request.POST, request.FILES)
            presupuesto_obtenido = get_object_or_404(Presupuesto, pk=id_p)  
            validar_presupuesto = Presupuesto.objects.filter(id=id_p, estado="Pendiente de contrato")
            if validar_presupuesto.exists():
                if form.is_valid():
                    # Guardar el Diseño
                    archivo = form.cleaned_data['archivo']
                    presupuesto_obtenido.estado="Enviado a producción"
                    presupuesto_obtenido.save()
                    pres = validar_presupuesto.first()  # O cualquier otra lógica para seleccionar un diseno de la lista
                    Orden_trabajo.objects.create(presupuesto=presupuesto_obtenido, contrato=archivo)
                    return redirect('/Presupuesto/')  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario
                else:
                    error = "No se puede adjuntar contrato"
                    return render(request, '404.html', {'error': error})
        else:
            form = ContratoForm()
            presupuesto = get_object_or_404(Presupuesto, pk=id_p)
            
            return render(request,'Designer/subir_diseno.html',{'form':form,'presupuesto':presupuesto})
        
#Rechazar presupuesto
@login_required(login_url='index')
def presupuesto_rechazar(request, pre_id,fin):
    # Obtener el presupuesto con el ID proporcionado
    presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
    if (fin==1):
        presupuesto.estado = "Rechazado"
    else:
        presupuesto.estado = "Entregado"
        
    presupuesto.fecha_fin = datetime.datetime.now()
    presupuesto.save()  # Guardar los cambios en la base de datos
    return redirect('/Presupuesto/')

#Rechazar diseño de presupuesto
@login_required(login_url='index')
def diseno_rechazar(request, pres_id, dis_id):
    # Obtener el diseño con el ID proporcionado
    diseno = get_object_or_404(Diseno, pk=dis_id)
    # Actualizar el estado del diseño
    diseno.estado = "Rechazado"
    diseno.save()  # Guardar los cambios en la base de datos
    
     # Obtener el presupuesto con el ID proporcionado
    presupuesto = get_object_or_404(Presupuesto, pk=pres_id)
     # Actualizar el estado del diseño
    presupuesto.estado = "Diseñando"
    presupuesto.save()  # Guardar los cambios en la base de datos
    return redirect('/Presupuesto/')

#Rechazar cotizacion de diseño
@login_required(login_url='index')
def cotizacion_rechazar(request, pres_id, coti_id):
    # Obtener la cotizacion con el ID proporcionado
    cotizacion = get_object_or_404(Cotizacion, pk=coti_id)
    # Actualizar el estado de la cotizacion
    cotizacion.estado = "Rechazado"
    cotizacion.save()  # Guardar los cambios en la base de datos
    
    # Obtener el presupuesto con el ID proporcionado
    presupuesto = get_object_or_404(Presupuesto, pk=pres_id)
     # Actualizar el estado del diseño
    presupuesto.estado = "Cotizando"
    presupuesto.save()  # Guardar los cambios en la base de datos
    return redirect('/Presupuesto/')

#Aprobar diseño de presupuesto
@login_required(login_url='index')
def diseno_aprobar(request, pres_id, dis_id):
    # Obtener el diseño con el ID proporcionado
    diseno = get_object_or_404(Diseno, pk=dis_id)
    # Actualizar el estado del diseño
    diseno.estado = "Aprobado"
    diseno.save()  # Guardar los cambios en la base de datos
    
     # Obtener el presupuesto con el ID proporcionado
    presupuesto = get_object_or_404(Presupuesto, pk=pres_id)
     # Actualizar el estado del diseño
    presupuesto.estado = "Cotizando"
    presupuesto.save()  # Guardar los cambios en la base de datos
    return redirect('/Presupuesto/')

#Aprobar cotizacion de diseño
@login_required(login_url='index')
def cotizacion_aprobar(request, pres_id, coti_id):
    # Obtener la cotizacion con el ID proporcionado
    cotizacion = get_object_or_404(Cotizacion, pk=coti_id)
    # Actualizar el estado de la cotización
    cotizacion.estado = "Aprobado"
    cotizacion.save()  # Guardar los cambios en la base de datos
    
     # Obtener el presupuesto con el ID proporcionado
    presupuesto = get_object_or_404(Presupuesto, pk=pres_id)
     # Actualizar el estado del diseño
    presupuesto.estado = "Pendiente de contrato"
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
        
        cotizaciones = Cotizacion.objects.filter(diseno__presupuesto=presupuesto)
        contratos = Orden_trabajo.objects.filter(presupuesto_id=presupuesto)
        return render(request,'Asesor/listado_disenos_presupuesto.html', {'presupuesto':presupuesto, 'pres': pres, 'cotizaciones': cotizaciones, 'contratos':contratos})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})


@login_required(login_url='index')
def disenos_presupuesto_fin(request, pre_id):
    user = request.user
    if (user.groups.filter(name='Asesor').exists() or user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Designer').exists()):
        # Obtener el presupuesto con el ID proporcionado
        presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
        
        #Lista de diseños del presupuesto
        pres = Diseno.objects.filter(presupuesto_id=presupuesto)
        
        cotizaciones = Cotizacion.objects.filter(diseno__presupuesto=presupuesto)
        contratos = Orden_trabajo.objects.filter(presupuesto_id=presupuesto)
        return render(request,'Asesor/listado_disenos_presupuesto_fin.html', {'presupuesto':presupuesto, 'pres': pres, 'cotizaciones': cotizaciones, 'contratos':contratos})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})

#Descargar archivo del contrato
def descargar_contrato(request, id):
    contrato = get_object_or_404(Orden_trabajo, pk=id)
    
    response = HttpResponse(contrato.contrato.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{contrato.contrato.name}"'
    
    return response
      
    