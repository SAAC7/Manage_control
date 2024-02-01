from django.urls import path
from . import views as cotizador_views

urlpatterns = [
    path('', cotizador_views.cotDisponibles , name='Cotizaciones'),
    path('Finalizados/', cotizador_views.cotFin , name='Cotizaciones_Finalizadas'),
    path('info/<pre_id>/', cotizador_views.info_cot , name='Cotizaciones_info'),
]