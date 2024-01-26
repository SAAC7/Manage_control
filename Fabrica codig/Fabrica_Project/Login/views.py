from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User , Group
from .forms import UserCreationForm


# Create your views here.

def index(request):
    return render(request,'Login/home.html')
def signin(request):
    if request.method=='GET':
        return render(request,'Login/signin.html')
    else:
        user = authenticate(request,username = request.POST['user'],password = request.POST['password'])
        if user is None:
            return render(request,'Login/signin.html',{
                'error': 'Usuaio o contraseña incorrectos'
            })
        else:
           login(request,user)
           return redirect ('/')
def signout(request):
    logout(request)
    return redirect ('/')
# Redirige a 'index' si el usuario no está autenticado
@login_required(login_url='index')
def usuarios(request):
    usuarios = User.objects.filter(is_superuser=False) 
    return render(request,'Login/user.html', {'usuarios': usuarios})




@login_required(login_url='index')
def crear_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Guardar la contraseña de forma segura
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Asignar el usuario al grupo seleccionado
            group = form.cleaned_data['group']
            group.user_set.add(user)
            return redirect('/')  # Redirigir a la página de inicio o donde desees
    else:
        form = UserCreationForm()
    return render(request, 'Login/user_create.html', {'form': form})


@login_required(login_url='index')
def usurario_desabilitar(requestm,user_id):
    # Obtener el usuario con el ID proporcionado
    user = get_object_or_404(User, pk=user_id)

    # Deshabilitar al usuario
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('/Usuarios/')  # Redirigir a la página de inicio o donde desees
