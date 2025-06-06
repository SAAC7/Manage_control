from django.urls import path
from . import views as asesor_views
from Disenadores import views as disenador_views

urlpatterns = [
    path('', asesor_views.listadoP , name='Presupuesto'),
    path('Finalizados/', asesor_views.listadoPF , name='PresupuestoFin'),
    path('Crear/', asesor_views.presupuesto , name='CrearPresupuesto'),
    path('Rechazar/<pre_id>/<fin>', asesor_views.presupuesto_rechazar , name='RechazarPresupuesto'),
    #Diseño
    path('Diseno/Rechazar/<int:pres_id>/<int:dis_id>/', asesor_views.diseno_rechazar, name='RechazarDiseno'),
    path('Diseno/Aprobar/<pres_id>/<dis_id>', asesor_views.diseno_aprobar , name='AprobarDiseno'),
    #Cotizacion
    path('Cotizacion/Rechazado/<int:pres_id>/<int:coti_id>/', asesor_views.cotizacion_rechazar , name='RechazarCotizacion'),
    path('Cotizacion/Aprobado/<pres_id>/<coti_id>', asesor_views.cotizacion_aprobar , name='AprobarCotizacion'),
    #Informacion
    path('Informacion/<pre_id>/', asesor_views.disenos_presupuesto , name='verInformacion'),
    path('Informacion/Finalizado/<pre_id>/', asesor_views.disenos_presupuesto_fin , name='verInformacionfin'),
    path('Informacion/Diseno/<diseno_id>/', asesor_views.listado_cotizaciones_diseno , name='verCotizaciones'),
    path('Informacion/Documentos-Produccion/<presupuesto_id>/', asesor_views.listado_documentos_produccion , name='verDocumentosProduccion'),
    #Contrato
    path('Contrato/<int:id_p>/', asesor_views.subir_contrato , name='subir_Contrato'),
    path('Contrato/Archivo/<int:id>/', asesor_views.descargar_contrato, name='descargar_contrato'),
    #Documentos de produccion
    path('Carta/Archivo/<int:id>/', asesor_views.descargar_carta, name='descargar_carta'),
    path('Hoja-Produccion/Archivo/<int:id>/', asesor_views.descargar_hoja_produccion, name='descargar_hoja_produccion'),
]