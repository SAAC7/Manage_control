from django.urls import path
from . import views as disenador_views

urlpatterns = [
    path('', disenador_views.listadoP , name='Diseno'),
    path('Enviado/', disenador_views.listadoPEnviados , name='Diseno_enviado'),
    path('SubirArchivo/<pre_id>', disenador_views.nuevo_diseno , name='subir_Diseno'),
    path('SubirArchivo/nuevo_diseno/<int:id_p>/', disenador_views.form_nuevo_diseno , name='subir_Diseno_nuevo'),
    path('descargar/<int:id>/', disenador_views.descargar_archivo, name='descargar_archivo'),
]