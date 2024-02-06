from django.db import models
from django.contrib.auth.models import User
from Asesores.models import Presupuesto

# Create your models here.
    
class Diseno_CNC(models.Model):
    disenador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='disenoCNC/', null=False, blank=False)
    
class Orden_trabajo(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT, null=False, blank=False)
    diseno_CNC = models.ForeignKey(Diseno_CNC, on_delete=models.PROTECT, null=True)
    contrato = models.FileField(upload_to='contratos/' ,null=False, blank=False)
    
class Trabajo(models.Model):
    trabajador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=False, blank=False)
    
class Trabajos_Orden(models.Model):
    orden = models.ForeignKey(Orden_trabajo, on_delete=models.PROTECT, null=False, blank=False)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT, null=False, blank=False)
    administrador = models.ForeignKey(User, on_delete=models.PROTECT, null=False)