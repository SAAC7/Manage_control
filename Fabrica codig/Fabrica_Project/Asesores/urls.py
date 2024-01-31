from django.urls import path
from . import views as asesor_views

urlpatterns = [
    path('', asesor_views.listadoP , name='Presupuesto'),
    path('Finalizados/', asesor_views.listadoPF , name='PresupuestoFin'),
    path('Crear/', asesor_views.presupuesto , name='CrearPresupuesto'),
    path('Rechazar/<pre_id>', asesor_views.presupuesto_rechazar , name='RechazarPresupuesto'),
    path('Informacion/<pre_id>', asesor_views.disenos_presupuesto , name='verInformacion'),
]