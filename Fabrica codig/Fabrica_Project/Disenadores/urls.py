from django.urls import path
from . import views as disenador_views

urlpatterns = [
    path('', disenador_views.listadoP , name='Diseno'),
    path('SubirArchivo/<pre_id>', disenador_views.nuevo_diseno , name='subir_Diseno'),
    path('Aprobar/<di_id>', disenador_views.aprovado_set , name='subir_Diseno'),
]