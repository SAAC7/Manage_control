from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Asesores.models import Presupuesto, Diseno
from .forms import DisenoForm
from django.http import HttpResponse


# Create your views here.
@login_required(login_url='index')
def listadoP(request):
    user = request.user
    if user.groups.filter(name='Designer').exists():
        pres = Presupuesto.objects.filter(fecha_fin=None, asesor=user, estado='Diseñando') 
        return render(request, 'Designer/listado_disenos_pendientes.html', {'pres': pres})
    elif (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        pres = Presupuesto.objects.filter(fecha_fin=None, estado='Diseñando') 
        return render(request, 'Designer/listado_disenos_pendientes.html', {'pres': pres})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})

#Crear Diseño
@login_required(login_url='index')
def nuevo_diseno(request, pre_id):
    user = request.user
    if (user.groups.filter(name='Asesor').exists() or user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Designer').exists()):
        form = DisenoForm()
        # Obtener el presupuesto con el ID proporcionado
        presupuesto = get_object_or_404(Presupuesto, pk=pre_id)
        
        #Lista de diseños del presupuesto
        pres = Diseno.objects.filter(presupuesto_id=presupuesto)
        
        if request.method == 'POST':
            form = DisenoForm(request.POST, request.FILES)
            if form.is_valid():
                # Guardar el Diseño
                archivo = form.cleaned_data['archivo']
                pres_id = form.cleaned_data['presupuesto_num']
                Diseno.objects.create(usuario=request.user, presupuesto=presupuesto, archivo=archivo, estado='Esperando aprobación')
                return redirect(request.path)  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario

        return render(request,'Designer/diseno.html', {'presupuesto':presupuesto, 'form':form, 'pres': pres})
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