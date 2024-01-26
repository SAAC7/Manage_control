from django.db import models
from Asesores.models import Presupuesto
from django.contrib.auth.models import User

# Create your models here.

class Cotizacion(models.Model):
    cotizador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='cotizaciones/', null=False, blank=False)