from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import datetime
from .models import *
from Asesores.models import Presupuesto, Diseno
from django.http import HttpResponse
from .forms import CotForm
# Create your views here.
#Cotizaciones disponibles
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
            
            # Verificar si hay reservaciones asociadas a este diseño
            # if diseño and not Reservacion.objects.filter(diseño=diseño).exists():
            #     # Si no hay reservaciones, agregar el presupuesto y el diseño a la lista
            presupuestos_con_diseños.append({'presupuesto': presupuesto, 'diseño': diseño})

        return render(request, 'Cotizador/listado.html', {'pres': presupuestos_con_diseños})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
   
@login_required(login_url='index')
def cotFin(request):
    return render(request, 'Cotizador/listado.html')

@login_required(login_url='index')
def info_cot(request, pre_id):
    user = request.user
    if (user.groups.filter(name='Cotizador').exists() or user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Designer').exists()):
        # Obtener el presupuesto con el ID proporcionado
        presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
        
        # Lista de diseños del presupuesto
        disenos = Diseno.objects.filter(presupuesto_id=presupuesto)
        
        # Obtener las cotizaciones del presupuesto
        cotizaciones = Cotizacion.objects.filter(diseno__presupuesto=presupuesto)
        
        return render(request, 'Cotizador/Cotizador_info.html', {'presupuesto': presupuesto, 'disenos': disenos, 'cotizaciones': cotizaciones})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
#Rechazar cotización
@login_required(login_url='index')
def presupuesto_rechazar(request, pre_id):
    # Obtener el presupuesto con el ID proporcionado
    presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
    # Actualizar el estado del presupuesto y la fecha de finalización
    presupuesto.estado = "Rechazado"
    presupuesto.fecha_fin = datetime.datetime.now()
    presupuesto.save()  # Guardar los cambios en la base de datos
    return redirect('/Presupuesto/')

@login_required(login_url='index')
def subir_cot(request,id_p):
    user = request.user
    if (user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Cotizador').exists()):
        if request.method == 'POST':
            form = CotForm(request.POST, request.FILES)
            presupuesto = get_object_or_404(Presupuesto, pk=id_p)  
            disenos = Diseno.objects.filter(presupuesto_id=presupuesto, estado="Aprobado")
            if disenos.exists():
                if form.is_valid():
                    # Guardar el Diseño
                    archivo = form.cleaned_data['archivo']
                    presupuesto.estado="Aprobando Cotización"
                    presupuesto.save()
                    diseno = disenos.first()  # O cualquier otra lógica para seleccionar un diseno de la lista
                    Cotizacion.objects.create(cotizador=user, diseno=diseno, archivo=archivo, estado='Esperando aprobación')
                    return redirect('/Cotizaciones/')  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario
                else:
                    error = "No se puede adjuntar Cotizacion"
                    return render(request, '404.html', {'error': error})
        else:
            form = CotForm()
            presupuesto = get_object_or_404(Presupuesto, pk=id_p)
            
            return render(request,'Designer/subir_diseno.html',{'form':form,'presupuesto':presupuesto})
        
def descargar_archivo(request, id):
    cotizacion = get_object_or_404(Cotizacion, id=id)
    
    # Obtener el archivo de la cotización
    archivo = cotizacion.archivo
    
    # Leer el contenido del archivo
    with archivo.open('rb') as f:
        contenido = f.read()
    
    # Crear la respuesta HTTP con el contenido del archivo
    response = HttpResponse(contenido, content_type='application/octet-stream')
    
    # Establecer el encabezado para la descarga del archivo
    response['Content-Disposition'] = f'attachment; filename="{archivo.name}"'
    
    return response
    
