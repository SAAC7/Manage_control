from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize


#Modelos
from .models import Orden_trabajo,Trabajo,Diseno_CNC,Trabajos_Orden
from Asesores.models import Presupuesto, Diseno
from Cotizadores.models import Cotizacion
from django.contrib.auth.models import Group, User



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
def ordenes_info(request, id_o):
    user = request.user
    if user.groups.filter(name='Administrador').exists() or user.is_superuser:
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
        return render(request, 'Produccion/Ordenes_trabajo_info.html',{'datos':objeto,'Trabajos':Trabajos_en_Orden,'trabajos_con_fecha_fin': trabajos_con_fecha_fin})
    else:
        error = "No tienes permiso para acceder a esta página."
        return render(request, '404.html', {'error': error})
    
    
    

def Asignar(request,id_orden):
    user = request.user
    if (user.groups.filter(name='Administrador').exists() or user.is_superuser):
        if request.method == 'POST':
            grupo_form = request.POST.get('grupo')
            trabajador_form = request.POST.get('integrante')
            commentario_form = request.POST.get('comment')
            
            trabajador_verificado=get_object_or_404(User,id=trabajador_form)
            grupo_verificado=get_object_or_404(Group,id=grupo_form)
            orden_verificado = get_object_or_404(Orden_trabajo, id=id_orden)
            
            
            new_trabajo = Trabajo.objects.create(trabajador=trabajador_verificado,grup=grupo_verificado,descripcion=commentario_form)
            new_trabajo_Orden = Trabajos_Orden.objects.create(administrador=user,trabajo=new_trabajo,orden=orden_verificado)
            return redirect('/Produccion/Ordenesinfo/{}'.format(id_orden))
            
            
        else:
        # Obtener todos los grupos excepto Administrador y Asesor
            grupos = Group.objects.exclude(name__in=['Administrador', 'Asesor','Designer','Cotizador'])
            # grupos = Group.objects.all()

            # Crear una lista de tuplas con el nombre y el ID de cada grupo
            # opciones_grupo = list(Group.objects.values_list('id', 'name'))
            opciones_grupo = list(grupos.values_list('id', 'name'))
            # Obtener el ID del grupo seleccionado, si hay uno
            usuarios  = User.objects.all()
            usuarios_serializados = serialize('json', usuarios)
            # Pasar las opciones del grupo y los integrantes al contexto del template
            
            orden = get_object_or_404(Orden_trabajo, id=id_orden)
            presupueto = get_object_or_404(Presupuesto,id=orden.presupuesto.id)  
            
            return render(request,'Produccion/Asignacion.html',{'grupos_user': opciones_grupo,'usuarios':usuarios_serializados,'presupueto':presupueto})


    else:
        error = "No se puede adjuntar contrato"
        return render(request, '404.html', {'error': error})

