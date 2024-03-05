from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.serializers import serialize
from django.utils import timezone
from .forms import *

#Modelos
from .models import *
from Asesores.models import Presupuesto, Diseno
from Cotizadores.models import Cotizacion
from django.contrib.auth.models import Group, User

#Lista de ordenes de trabajo disponibles
@login_required(login_url='index')
def ordenes_listado(request,fin):
    user = request.user
    if (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        lista_Ordenes=[]
        if (fin==1):
            ordenes = Orden_trabajo.objects.filter(fecha_Entregado__isnull=False)
        else:
            ordenes = Orden_trabajo.objects.filter(fecha_Entregado__isnull=True)
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
        {'lista_Ordenes': lista_Ordenes, 'finalizados':fin}
        )
    
        
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})

#Listado de hojas de produccion que necesitan diseño CNC
@login_required(login_url='index')
def listado_Diseno_CNC_pendiente(request):
    hojas = Hoja_de_Produccion.objects.filter() 
    return render(request,'Produccion/disenos_cnc_pendientes.html',{'hojas':hojas})

#Listado de hojas de produccion que necesitan diseño CNC
@login_required(login_url='index')
def listado_Diseno_CNC_enviados(request):
    hojas = Hoja_de_Produccion.objects.filter(estado='Enviado a producción') 
    return render(request,'Produccion/disenos_cnc_enviados.html',{'hojas':hojas})
    
@login_required(login_url='index')        
def trabajo(request):
    usuario_autenticado = request.user
    if (usuario_autenticado.groups.filter(name='Administrador').exists() or usuario_autenticado.is_superuser):
        trabajos = Trabajo.objects.filter(fecha_fin__isnull=True)
        return render(request, 'Produccion/trabajos.html', {'trabajos': trabajos})
    elif not usuario_autenticado.groups.filter(name__in=['Administrador', 'Superusuario', 'Designer', 'Asesor', 'Cotizador']).exists():
        trabajos = Trabajo.objects.filter(trabajador=usuario_autenticado,fecha_fin__isnull=True)
        return render(request, 'Produccion/trabajos.html', {'trabajos': trabajos})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
@login_required(login_url='index')    
def trabajofin(request):
    usuario_autenticado = request.user
    if not (usuario_autenticado.groups.filter(name__in=['Administrador', 'Designer', 'Asesor', 'Cotizador']).exists() or usuario_autenticado.is_superuser):
        # trabajos_listado = Trabajo.objects.filter(trabajador=usuario_autenticado,fecha_fin__isnull=False)
        trabajos_listado = Trabajos_Orden.objects.filter(trabajo__trabajador=usuario_autenticado,trabajo__fecha_fin__isnull=False)
        print("1")
        return render(request, 'Produccion/trabajos_finalizados.html', {'trabajos': trabajos_listado})
    elif (usuario_autenticado.groups.filter(name='Administrador').exists() or usuario_autenticado.is_superuser):
        # trabajos_listado = Trabajo.objects.filter(fecha_fin__isnull=False)
        trabajos_listado = Trabajos_Orden.objects.filter(trabajo__fecha_fin__isnull=False)
        print("2")
        return render(request, 'Produccion/trabajos_finalizados.html', {'trabajos': trabajos_listado})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})

#Trabajos y hojas de produccion asociadas a una orden de trabajo
@login_required(login_url='index')    
def ordenes_info(request, id_o,fin):
    user = request.user
    if user :
        orden = get_object_or_404(Orden_trabajo, id=id_o)
        diseno_aprobado = Diseno.objects.filter(presupuesto=orden.presupuesto, estado='Aprobado').first()  \
        # Filtrar las hojas de producción asociadas a esa orden de trabajo
        hojas_produccion = orden.hojaproduccion.all()
        
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
        
        Trabajos_en_Orden = Trabajos_Orden.objects.filter(orden=orden)
        trabajos_con_fecha_fin = Trabajos_en_Orden.filter(trabajo__fecha_fin__isnull=True).exists()
        
        # Pasa la cotización al contexto del template para que pueda ser renderizada
        if (fin==1):
            return render(request, 'Produccion/Ordenes_trabajo_info_fin.html',{'datos':objeto,'Trabajos':Trabajos_en_Orden,'trabajos_con_fecha_fin': trabajos_con_fecha_fin, 'hojas_produccion': hojas_produccion})
        else:
            return render(request, 'Produccion/Ordenes_trabajo_info.html',{'datos':objeto,'Trabajos':Trabajos_en_Orden,'trabajos_con_fecha_fin': trabajos_con_fecha_fin, 'hojas_produccion': hojas_produccion})
            
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})

#Asignar trabajo a un trabajador   
@login_required(login_url='index')  
def Asignar(request,id_orden):
    user = request.user
    if (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        if request.method == 'POST':
            grupo_form = request.POST.get('grupo')
            trabajador_form = request.POST.get('integrante')
            commentario_form = request.POST.get('comment')
            fecha_programada_form = request.POST.get('fecha_program')
            
            trabajador_verificado=get_object_or_404(User,id=trabajador_form)
            grupo_verificado=get_object_or_404(Group,id=grupo_form)
            orden_verificado = get_object_or_404(Orden_trabajo, id=id_orden)
            
            
            new_trabajo = Trabajo.objects.create(trabajador=trabajador_verificado,grup=grupo_verificado,descripcion=commentario_form,fecha_programada=fecha_programada_form)
            new_trabajo_Orden = Trabajos_Orden.objects.create(administrador=user,trabajo=new_trabajo,orden=orden_verificado)
            return redirect('/Produccion/Ordenes/Informacion/{}'.format(id_orden)+'/0')
            
            
        else:
        # Obtener todos los grupos excepto Administrador y Asesor
            grupos = Group.objects.exclude(name__in=['Administrador', 'Asesor','Designer','Cotizador'])
            # grupos = Group.objects.all()

            # Crear una lista de tuplas con el nombre y el ID de cada grupo
            # opciones_grupo = list(Group.objects.values_list('id', 'name'))
            opciones_grupo = list(grupos.values_list('id', 'name'))
            # Obtener el ID del grupo seleccionado, si hay uno
            usuarios  = User.objects.filter(is_active=True)
            usuarios_serializados = serialize('json', usuarios)
            # Pasar las opciones del grupo y los integrantes al contexto del template
            
            orden = get_object_or_404(Orden_trabajo, id=id_orden)
            presupueto = get_object_or_404(Presupuesto,id=orden.presupuesto.id)  
            
            return render(request,'Produccion/Asignacion.html',{'grupos_user': opciones_grupo,'usuarios':usuarios_serializados,'presupueto':presupueto})


    else:
        error = "No se puede adjuntar contrato"
        return render(request, '404.html', {'error': error})

#Subir diseño CNC y de Producción a la hoja de producción
@login_required(login_url='index')
def subir_CNC_produccion(request,id_h):
    user = request.user
    if (user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Cotizador').exists()):
        if request.method == 'POST':
            form = DisenoCNCForm(request.POST, request.FILES)
            form2 = DisenoProduccionForm(request.POST, request.FILES)
            hoja_obtenida = get_object_or_404(Hoja_de_Produccion, pk=id_h)  
            validar_hoja = Hoja_de_Produccion.objects.filter(id=id_h)
            if validar_hoja.exists():
                if form.is_valid() and form2.is_valid():
                    # Guardar el Diseño
                    cnc = form.cleaned_data['archivo_cnc']
                    diseno = form2.cleaned_data['archivo']
                    
                    hoja_obtenida.estado="Enviado a producción"
                    hoja_obtenida.save()
                    pres = validar_hoja.first()  # O cualquier otra lógica para seleccionar un diseno de la lista
                    diseno_cnc =Diseno_CNC.objects.create(archivo=cnc, disenador=user)
                    diseno_cnc.save()
                    diseno_produccion =Diseno_Produccion.objects.create(archivo=diseno, disenador=user, estado="Enviado a producción")
                    diseno_produccion.save()
                    
                    hoja_obtenida.diseno_CNC_id = diseno_cnc.id
                    hoja_obtenida.diseno_produccion_id = diseno_produccion.id
                    hoja_obtenida.save()
                    return redirect('/Produccion/Diseno-CNC/Pendientes')  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario
                else:
                    error = "No se puede adjuntar contrato"
                    return render(request, '404.html', {'error': error})
        else:
            form = DisenoCNCForm()
            hoja = get_object_or_404(Hoja_de_Produccion, pk=id_h)
            
            return render(request,'Produccion/subir_cnc.html',{'form':form,'presupuesto':hoja})

#Finalizar trabajo 
@login_required(login_url='index')     
def finalizar_trabajo(request,id_t):
    user = request.user
    trabajos = get_object_or_404(Trabajo,id=id_t)
    trabajos.fecha_fin = timezone.now()
    trabajos.save()                        
    return redirect('/Produccion/Trabajos/')

#Descargar archivo de diseño
@login_required(login_url='index')
def descargar_diseno(request, id_o):
    # Obtén la orden de trabajo por su ID
    orden = get_object_or_404(Orden_trabajo,id=id_o)
    
    # Obtén el diseño CNC relacionado con la orden de trabajo
    diseno = orden.diseno_CNC
    
    # Abre el archivo en modo lectura binaria
    archivo = open(diseno.archivo.path, 'rb')
    
    # Crea una respuesta con el archivo
    response = FileResponse(archivo)
    
    return response

@login_required(login_url='index')
def finalizar_orden(request,id_o):
    orden = get_object_or_404(Orden_trabajo,id=id_o)
    orden.fecha_Entregado=timezone.now()
    orden.save()
    return redirect('/Produccion/Ordenes-de-Trabajo/0/')

#Descargar archivo de la hoja de producción
@login_required(login_url='index')
def hoja_produccion(request, id):
    hojas_produccion = get_object_or_404(Hoja_de_Produccion, pk=id)
    
    response = HttpResponse(hojas_produccion.archivo.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{hojas_produccion.archivo.name}"'
    
    return response

#Descargar archivo del diseño de producción
@login_required(login_url='index')
def diseno_produccion(request, id):
    hoja_de_produccion = get_object_or_404(Hoja_de_Produccion, pk=id)
    diseno_produccion = hoja_de_produccion.diseno_produccion
    
    response = HttpResponse(diseno_produccion.archivo.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{diseno_produccion.archivo.name}"'
    
    return response

#Descargar archivo del diseño cnc
@login_required(login_url='index')
def diseno_cnc(request, id):
    hoja_de_produccion = get_object_or_404(Hoja_de_Produccion, pk=id)
    diseno_cnc = hoja_de_produccion.diseno_CNC
    
    response = HttpResponse(diseno_cnc.archivo.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{diseno_cnc.archivo.name}"'
    
    return response

#Descargar archivo del contrato
def descargar_contrato(request, id):
    contrato = get_object_or_404(Orden_trabajo, pk=id)
    
    response = HttpResponse(contrato.contrato.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{contrato.contrato.name}"'
    
    return response

def aceptar_orden(request, id_o):
    orden = get_object_or_404(Orden_trabajo, pk=id_o)
    presupuesto = get_object_or_404(Presupuesto, pk=orden.presupuesto.id)
    presupuesto.estado = "Produciendo"  
    presupuesto.save()
    
    
    datos_post = {
        'grupo': 'valor1',
        'integrante': 'valor2',
        'comment': 'valor2',
        'fecha_program': 'valor2',
        }

    # Redirigir a la vista 'TrabajosCrear' con el parámetro id_orden y los datos POST
    error = datos_post
    return render(request, '404.html', {'error': error})
    # return redirect('TrabajosCrear', id_orden=id_o, data=post_data, method='POST')
