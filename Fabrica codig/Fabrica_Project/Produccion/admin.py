from django.contrib import admin

# Register your models here.
from .models import Orden_trabajo,Trabajo,Diseno_CNC,Trabajos_Orden

# Register your models here.
admin.site.register(Orden_trabajo)
admin.site.register(Trabajo)
admin.site.register(Diseno_CNC)
admin.site.register(Trabajos_Orden)