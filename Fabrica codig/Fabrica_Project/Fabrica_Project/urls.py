"""
URL configuration for Fabrica_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Login import views as login_views
from Asesores import views as asesor_views
from Produccion import views as produccion_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.index , name='index'),
    path('signin/', login_views.signin , name='signin'),
    path('signout/', login_views.signout , name='signout'),
    path('Usuarios/', login_views.usuarios , name='usuarios'),
    path('Usuarios/Crear/', login_views.crear_usuario , name='usuarios_crear'),
    path('Usuarios/Desabilitar/<user_id>', login_views.usurario_desabilitar , name='usuarios_crear'),
    path('Presupuesto/', asesor_views.listadoP , name='Presupuesto'),
    path('Presupuesto/Finalizados/', asesor_views.listadoPF , name='PresupuestoFin'),
    path('Presupuesto/Crear/', asesor_views.presupuesto , name='CrearPresupuesto'),
    path('Presupuesto/Rechazar/<pre_id>', asesor_views.presupuesto_rechazar , name='RechazarPresupuesto'),
    path('Trabajos/', produccion_views.trabajo , name='Trabajos'),
    
]
