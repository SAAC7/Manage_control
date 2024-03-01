from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.serializers import serialize
from django.utils import timezone
from forms import DisenoCNCForm, DisenoProduccionForm, HojaProduccionUpdateForm

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

#Listado de presupuestos que necesitan diseño CNC
@login_required(login_url='index')
def listado_Diseno_CNC_pendiente(request):
    hojas = Hoja_de_Produccion.objects.filter(estado='Esperando diseño CNC') 
    return render(request,'Produccion/disenos_cnc_pendientes.html',{'hojas':hojas})
    
@login_required(login_url='index')        
def trabajo(request):
    usuario_autenticado = request.user
    if (usuario_autenticado.groups.filter(name='Administrador').exists() or usuario_autenticado.is_superuser):
        print("1")
        trabajos = Trabajo.objects.filter(fecha_fin__isnull=True)
        return render(request, 'Produccion/trabajos.html', {'trabajos': trabajos})
    elif not usuario_autenticado.groups.filter(name__in=['Administrador', 'Superusuario', 'Designer', 'Asesor', 'Cotizador']).exists():
        print("2")
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
    
@login_required(login_url='index')    
def ordenes_info(request, id_o,fin):
    user = request.user
    if user :
        orden = get_object_or_404(Orden_trabajo, id=id_o)
        diseno_aprobado = Diseno.objects.filter(presupuesto=orden.presupuesto, estado='Aprobado').first()  
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
            return render(request, 'Produccion/Ordenes_trabajo_info_fin.html',{'datos':objeto,'Trabajos':Trabajos_en_Orden,'trabajos_con_fecha_fin': trabajos_con_fecha_fin})
        else:
            return render(request, 'Produccion/Ordenes_trabajo_info.html',{'datos':objeto,'Trabajos':Trabajos_en_Orden,'trabajos_con_fecha_fin': trabajos_con_fecha_fin})
            
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
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
            return redirect('/Produccion/Ordenesinfo/{}'.format(id_orden)+'/0')
            
            
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

#Subir diseno CNC y diseño de produccion
@login_required(login_url='index')
def subir_contrato(request,id_h):
    user = request.user
    if (user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Cotizador').exists()):
        if request.method == 'POST':
            form = DisenoCNCForm(request.POST, request.FILES)
            form2 = DisenoProduccionForm(request.POST, request.FILES)
            hoja_obtenida = get_object_or_404(Hoja_de_Produccion, pk=id_h)  
            validar_hoja = Presupuesto.objects.filter(id=id_h, estado="Esperando diseño CNC")
            if validar_hoja.exists():
                if form.is_valid() and form2.is_valid():
                    # Guardar el Diseño
                    cnc = form.cleaned_data['archivo']
                    diseno = form2.cleaned_data['archivo']
                    hojasform=request.FILES.getlist('archivos')
                    
                    hoja_obtenida.estado="Enviado a producción"
                    hoja_obtenida.save()
                    pres = validar_hoja.first()  # O cualquier otra lógica para seleccionar un diseno de la lista
                    
                    diseno_cnc =Diseno_CNC.objects.create(archivo=cnc, disenador_id=User.objects.get(id=user.id))
                    diseno_produccion =Diseno_Produccion.objects.create(archivo=diseno, disenador_id=User.objects.get(id=user.id))
                    diseno_cnc.save()
                    diseno_produccion.save()
                    
                    return redirect('/Presupuesto/')  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario
                else:
                    error = "No se puede adjuntar contrato"
                    return render(request, '404.html', {'error': error})
        else:
            form = ContratoForm()
            presupuesto = get_object_or_404(Presupuesto, pk=id_p)
            
            return render(request,'Asesor/subir_documentos_finales.html',{'form':form,'presupuesto':presupuesto})
        
# @login_required(login_url='index')  
# def subir_diseno_cnc(request,id_o):
#     user = request.user
#     if (user.groups.filter(name='Administrador').exists() or user.is_superuser or user.groups.filter(name='Designer_CNC').exists()):
#         if request.method == 'POST':
        
#             form = coti_form.CotForm(request.POST, request.FILES)
#             orden_de_trabajo = get_object_or_404(Orden_trabajo, pk=id_o)  
#             if form.is_valid():
#                 archivo = form.cleaned_data['archivo']
    
#                 # Crear una nueva instancia de Diseno_CNC y guardar el archivo allí
#                 diseno_cnc = Diseno_CNC(archivo=archivo,disenador=user)
#                 diseno_cnc.save()
                
#                 # Ahora puedes asignar la instancia de Diseno_CNC a orden_de_trabajo.diseno_CNC
#                 orden_de_trabajo.diseno_CNC = diseno_cnc
#                 orden_de_trabajo.save()
                
#                  # Busca los trabajos asociados a esa orden de trabajo donde el grupo es 'Designer_CNC'
#                 trabajos_ord = Trabajos_Orden.objects.filter(orden=orden_de_trabajo, trabajo__grup__name='Designer_CNC')

#                 # Extrae los objetos Trabajo de los Trabajos_Orden
#                 for trabajo_ord in trabajos_ord:
#                     trabajo = get_object_or_404(Trabajo, id=trabajo_ord.trabajo.id)
#                     trabajo.fecha_fin = timezone.now()
#                     trabajo.save()

                
                
                    
#                 return redirect('/Produccion/Trabajos/')  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario
#             else:
#                 error = "No se puede adjuntar Cotizacion"
#                 return render(request, '404.html', {'error': error})
#         else:
#             form = coti_form.CotForm(request.POST, request.FILES)
#             orden_de_trabajo = get_object_or_404(Orden_trabajo, pk=id_o) 
#             print(orden_de_trabajo)
            
#             return render(request,'Designer/subir_diseno.html',{'form':form,'presupuesto':orden_de_trabajo})
#     else:
#         error = "No tienes permiso para acceder a esta página."
#         return render(request, '404.html', {'error': error})
    
@login_required(login_url='index')     
def finalizar_trabajo(request,id_t):
    user = request.user
    trabajos = get_object_or_404(Trabajo,id=id_t)
    trabajos.fecha_fin = timezone.now()
    trabajos.save()                        
    return redirect('/Produccion/Trabajos/')

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

@login_required(login_url='index')
def descargar_hoja_produccion(request, id):
    hojas_produccion = get_object_or_404(Hoja_de_Produccion, pk=id)
    
    response = HttpResponse(hojas_produccion.archivo.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{hojas_produccion.archivo.name}"'
    
    return response
    
#Descargar archivo del contrato
def descargar_contrato(request, id):
    contrato = get_object_or_404(Orden_trabajo, pk=id)
    
    response = HttpResponse(contrato.contrato.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{contrato.contrato.name}"'
    
    return response