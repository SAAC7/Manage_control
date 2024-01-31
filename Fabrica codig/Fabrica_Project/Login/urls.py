from django.urls import path
from . import views as login_views

urlpatterns = [
    path('', login_views.index , name='index'),
    path('signin/', login_views.signin , name='signin'),
    path('signout/', login_views.signout , name='signout'),
    path('Usuarios/', login_views.usuarios , name='usuarios'),
    path('Usuarios/Crear/', login_views.crear_usuario , name='usuarios_crear'),
    path('Usuarios/Desabilitar/<user_id>', login_views.usurario_desabilitar , name='usuarios_crear'),
]