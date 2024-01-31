from django.db import models
from Asesores.models import Presupuesto,Diseno
from django.contrib.auth.models import User

# Create your models here.

class Cotizacion(models.Model):
    cotizador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    estado=models.TextField(null=True, blank=True, default='Esperando aprobación')
    archivo = models.FileField(upload_to='cotizaciones/', null=False, blank=False)

# class Reservacion(models.Model):
#     fecha_de_reserva = models.DateTimeField(auto_now_add=True)
#     diseño = models.ForeignKey(Diseno, on_delete=models.PROTECT, null=False, blank=False)
#     cotizacion=models.ForeignKey(Cotizacion, on_delete=models.PROTECT, null=True, blank=True)

    