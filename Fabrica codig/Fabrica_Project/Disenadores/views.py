from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Asesores.models import Presupuesto, Diseno
from Cotizadores.models import Cotizacion
from .forms import DisenoForm
from django.http import HttpResponse


#Listado de presupuestos con diseño pendiente de asignar
@login_required(login_url='index')
def listadoP(request):
    user = request.user
    if user.groups.filter(name='Designer').exists():
        pres = Presupuesto.objects.filter(fecha_fin=None, estado='Diseñando') 
        return render(request, 'Designer/listado_disenos_pendientes.html', {'pres': pres})
    elif (user.groups.filter(name='Administrador').exists()):
        pres = Presupuesto.objects.filter(fecha_fin=None, asesor=user, estado='Diseñando') 
        return render(request, 'Designer/listado_disenos_pendientes.html', {'pres': pres})
    elif (user.is_superuser):
        pres = Presupuesto.objects.filter(fecha_fin=None, estado='Diseñando') 
        return render(request, 'Designer/listado_disenos_pendientes.html', {'pres': pres})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})

#Listado de presupuestos a los que ya se les asigno diseño
@login_required(login_url='index')
def listadoPEnviados(request):
    user = request.user
    if user.groups.filter(name='Designer').exists():
        disenos = Diseno.objects.select_related('presupuesto').filter(user=user).exclude(estado="Diseño guía")
        return render(request, 'Designer/listado_disenos_enviados.html', {'disenos': disenos})
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        disenos = Diseno.objects.select_related('presupuesto').exclude(estado="Diseño guía")
        return render(request, 'Designer/listado_disenos_enviados.html', {'disenos': disenos})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
#Crear Diseño
@login_required(login_url='index')
def nuevo_diseno(request, pre_id):
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
    
#Redireccionar y obtener id del presupuesto
@login_required(login_url='index')
def obtener_presupuesto_id(request, pre_id):
    # Obtener el presupuesto con el ID proporcionado
    presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
    return redirect('/SubirArchivo/', presupuesto)

#Descargar archivo del registro especificado
def descargar_archivo(request, id):
    diseno = get_object_or_404(Diseno, id=id)
    
    response = HttpResponse(diseno.archivo.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{diseno.archivo.name}"'
    
    return response
    
    #return redirect('/Diseno/SubirArchivo/'+ str(diseno.presupuesto.id))
    
#Descargar archivo del registro especificado
def descargar_coti(request, id):
    cotizacion = get_object_or_404(Cotizacion, id=id)
    
    response = HttpResponse(cotizacion.archivo.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{cotizacion.archivo.name}"'
    
    return response

#Form para subir nuevo diseño
def form_nuevo_diseno(request,id_p):
    user = request.user
    if (user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Designer').exists()):
        if request.method == 'POST':
            form = DisenoForm(request.POST, request.FILES)
            if form.is_valid():
                # Guardar el Diseño
                archivo = form.cleaned_data['archivo']
                presupuesto = get_object_or_404(Presupuesto, pk=id_p)  
                presupuesto.estado="Aprobando Diseño"
                presupuesto.save()
                
                Diseno.objects.create(usuario=request.user, presupuesto=presupuesto, archivo=archivo, estado='Esperando aprobación')
                
                return redirect('/Diseno/')  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario
        else:
            form = DisenoForm()
            presupuesto = get_object_or_404(Presupuesto, pk=id_p)
            
            return render(request,'Designer/subir_diseno.html',{'form':form,'presupuesto':presupuesto})