from django.db import models
from Asesores.models import Presupuesto,Diseno
from django.contrib.auth.models import User

# Create your models here.

class Cotizacion(models.Model):
    cotizador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    diseno = models.ForeignKey(Diseno, on_delete=models.PROTECT, null=True, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_cambio = models.DateTimeField(null=True, blank=True)
    estado=models.TextField(null=True, blank=True, default='Esperando aprobación')
    comentario=models.TextField(null=True, blank=True)
    archivo = models.FileField(upload_to='media/cotizaciones/', null=False, blank=False)

