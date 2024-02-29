from django.urls import path
from . import views as produccion_views

urlpatterns = [
    path('Ordenes-de-Trabajo/<int:fin>/', produccion_views.ordenes_listado , name='OrdenesDeTrabajo'),
    path('Ordenesinfo/<int:id_o>/<int:fin>/', produccion_views.ordenes_info , name='ordenes_trabajo_info'),
    path('Ordenesinfo/Finalizar/<int:id_o>/', produccion_views.finalizar_orden , name='ordenes_trabajo_fin'),
    path('Ordenesinfo/Descargar/<int:id_o>/<int:tipo>/', produccion_views.descargar_hoja_produccion , name='descargar_cnc'),
    path('Contrato/Archivo/<int:id>/', produccion_views.descargar_contrato, name='descargar_contrato'),
    path('Trabajos/', produccion_views.trabajo , name='Trabajos'),
    path('Trabajos/Crear/<int:id_orden>', produccion_views.Asignar , name='TrabajosCrear'),
    path('Trabajos/Finalizados/', produccion_views.trabajofin , name='Trabajos_finalizados'),
    path('Trabajos/SubirdienoCNC/<int:id_o>/', produccion_views.subir_diseno_cnc , name='diseno_cnc'),
    path('Trabajos/Finalizar/<int:id_t>/', produccion_views.finalizar_trabajo , name='finalizar_trabajo'),
]
