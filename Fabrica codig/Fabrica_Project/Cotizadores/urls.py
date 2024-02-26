from django.urls import path
from . import views as cotizador_views
from Asesores import views as asesor_views

urlpatterns = [
    path('', cotizador_views.cotDisponibles , name='Cotizaciones'),
    path('Finalizados/', cotizador_views.cotFin , name='Cotizaciones_Finalizadas'),
    path('Informacion/<pre_id>/', cotizador_views.info_cot , name='Cotizaciones_info'),
    path('Informacion/Diseno/<diseno_id>/', asesor_views.listado_cotizaciones_diseno , name='verCotizaciones'),
    path('SubirArchivo/Nueva_Cotizacion/<int:id_p>/', cotizador_views.subir_cot , name='subir_Cotizacion_nuevo'),
    path('descargar/<int:id>/', cotizador_views.descargar_archivo, name='descargar_archivo_Cotizacion'),
]