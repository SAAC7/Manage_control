from django.urls import path
from . import views as produccion_views

urlpatterns = [
    path('Ordenes-de-Trabajo/<int:fin>/', produccion_views.ordenes_listado , name='OrdenesDeTrabajo'),
    path('Ordenes-de-Trabajo/Aceptar/<int:id_o>/', produccion_views.aceptar_orden , name='aceptarOrdenes'),
    path('Ordenes/Informacion/<int:id_o>/<int:fin>/', produccion_views.ordenes_info , name='ordenes_trabajo_info'),
    path('Ordenes/Informacion/Finalizar/<int:id_o>/', produccion_views.finalizar_orden , name='ordenes_trabajo_fin'),
    path('Ordenes/Informacion/Descargar/<int:id_o>/<int:tipo>/', produccion_views.hoja_produccion , name='descargar_cnc'),
    path('Contrato/Archivo/<int:id>/', produccion_views.descargar_contrato, name='descargar_contrato'),
    path('Trabajos/', produccion_views.trabajo , name='Trabajos'),
    path('Trabajos/Crear/<int:id_orden>', produccion_views.Asignar , name='TrabajosCrear'),
    path('Trabajos/Finalizados/', produccion_views.trabajofin , name='Trabajos_finalizados'),
    path('Trabajos/Finalizar/<int:id_t>/', produccion_views.finalizar_trabajo , name='finalizar_trabajo'),
    path('Diseno-CNC/', produccion_views.listado_Diseno_CNC_pendiente , name='cnc_pendientes'),
    path('Diseno-CNC/Enviados', produccion_views.listado_Diseno_CNC_enviados , name='cnc_listos'),
    path('Diseno-CNC/Diseno/<int:id>', produccion_views.diseno_produccion , name='produccion_descargar'),
    path('Diseno-CNC/CNC/<int:id>', produccion_views.diseno_cnc , name='cnc_descargar'),
    path('Hoja-Produccion/Archivo/<int:id>/', produccion_views.hoja_produccion , name='descargar_hoja-produccion'),
    path('CNC/<int:id_h>/', produccion_views.subir_CNC_produccion , name='subir_Contrato'),
]
