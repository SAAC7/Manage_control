from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(Orden_trabajo)
admin.site.register(Trabajo)
admin.site.register(Diseno_CNC)
admin.site.register(Diseno_Produccion)
admin.site.register(Hoja_de_Produccion)
admin.site.register(Contrato)
admin.site.register(Trabajos_Orden)