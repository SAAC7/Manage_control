from django.urls import path
from . import views as produccion_views

urlpatterns = [
    path('Ordenes-de-Trabajo', produccion_views.ordenes_listado , name='OrdenesDeTrabajo'),
    path('Trabajos/', produccion_views.trabajo , name='Trabajos'),
    path('Trabajos/Finalizados/', produccion_views.trabajofin , name='Trabajos_finalizados'),
]
