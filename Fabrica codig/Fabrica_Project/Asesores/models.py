from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Presupuesto(models.Model):
    asesor = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    fecha_inicio = models.DateTimeField(null=False, auto_now_add=True, blank=False)
    fecha_fin = models.DateTimeField(null=True, blank=True)    
    
class Diseno(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(null=False, blank=False)    