from django.contrib import admin

# Register your models here.
from .models import *


class Hoja_de_ProduccionAdmin(admin.ModelAdmin):
    # Lista de campos que quieres que sean opcionales al crear una nueva instancia
    fields = ['disenador', 'estado','diseno_CNC','diseno_produccion','archivo']

    # Excluir el campo fecha
    exclude = ['fecha']


# Registrar el modelo y el admin
admin.site.register(Hoja_de_Produccion, Hoja_de_ProduccionAdmin)

admin.site.register(Orden_trabajo)
admin.site.register(Trabajo)
admin.site.register(Diseno_CNC)
admin.site.register(Diseno_Produccion)
admin.site.register(Contrato)
admin.site.register(Trabajos_Orden)