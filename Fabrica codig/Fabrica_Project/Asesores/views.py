from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import Presupuesto, Diseno

# Create your views here.
@login_required(login_url='index')
def presupuesto(request):
    return render(request,'Asesor/presupuesto.html')
@login_required(login_url='index')
def listadoP(request):
    return render(request,'Asesor/listado_presupuesto.html')

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
        