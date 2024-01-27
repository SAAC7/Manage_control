from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import Presupuesto, Diseno
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
# Create your views here.
@login_required(login_url='index')
def listadoP(request):
    return render(request,'Asesor/listado_presupuesto.html')

from django.shortcuts import render, redirect
from .models import Presupuesto, Diseno
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

@login_required
def presupuesto(request):
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombreCliente')
        descripcion = request.POST.get('descripcion')
        asesor = request.user  # Suponiendo que el usuario actual es el asesor
        necesita_diseno=request.POST.get('solDesign')

        # Guardar los datos en el modelo Presupuesto
        presupuesto = Presupuesto.objects.create(
            asesor=asesor,
            cliente=nombre_cliente,
            descripcion=descripcion
        )

        # Verificar si se marcó la casilla de mandar a diseñar

        mi_archivo = request.FILES['miArchivo1']
        diseno = Diseno.objects.create(
            usuario=request.user,
            presupuesto=presupuesto,
            necesita_diseno=necesita_diseno,
            archivo=mi_archivo
        )

        return redirect('/Presupuesto/')  # Cambia 'ruta_de_redireccion' por la URL a la que deseas redirigir después de procesar el formulario
    else:
        return render(request, 'Asesor/presupuesto.html')  # Cambia 'nombre_del_template.html' por el nombre de tu template donde está el formulario
