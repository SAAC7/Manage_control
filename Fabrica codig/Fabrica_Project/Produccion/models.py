from django.db import models
from django.contrib.auth.models import User,Group

from Asesores.models import Presupuesto

# Create your models here.
    
class Diseno_CNC(models.Model):
    disenador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='media/disenoCNC/', null=False, blank=False)
    
class Diseno_Produccion(models.Model):
    disenador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    estado=models.TextField(null=True, blank=True)
    archivo = models.FileField(upload_to='media/disenoProduccion/', null=False, blank=False)
    
class Orden_trabajo(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT, null=False, blank=False)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_Entregado = models.DateTimeField(null=True, blank=True)
    contrato = models.FileField(upload_to='media/contratos/')
    carta = models.FileField(upload_to='media/carta/')
    hojaproduccion = models.ManyToManyField('Hoja_de_Produccion', blank=True)
    
class Hoja_de_Produccion(models.Model):
    disenador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    estado=models.TextField(default='Esperando diseño CNC', null=True, blank=True)
    diseno_CNC = models.ForeignKey(Diseno_CNC, on_delete=models.PROTECT, null=True,blank=True) 
    diseno_produccion = models.ForeignKey(Diseno_Produccion, on_delete=models.PROTECT, null=True,blank=True)
    archivo = models.FileField(upload_to='media/Produccion/')

class Contrato(models.Model):
    disenador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    estado=models.TextField(null=True, blank=True)
    archivo = models.FileField(upload_to='media/contratos/')
    
class Trabajo(models.Model):
    trabajador = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    grup = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_programada=models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=False, blank=False)
    
class Trabajos_Orden(models.Model):
    orden = models.ForeignKey(Orden_trabajo, on_delete=models.PROTECT, null=False, blank=False)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT, null=False, blank=False)
    administrador = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    
    
    
