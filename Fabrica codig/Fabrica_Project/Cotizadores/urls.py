from django.urls import path
from . import views as cotizador_views

urlpatterns = [
    path('', cotizador_views.cotDisponibles , name='Cotizaciones'),
    path('Reservadas/', cotizador_views.cotReservadas , name='Cotizaciones_Reservadas'),
    path('Finalizados/', cotizador_views.cotFin , name='Cotizaciones_Finalizadas'),
]