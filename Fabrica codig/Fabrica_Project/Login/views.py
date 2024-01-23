from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# Create your views here.
# Redirige a 'index' si el usuario no está autenticado
# @login_required(login_url='index')
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
def tablas(request):
    return render(request,'Login/table.html')