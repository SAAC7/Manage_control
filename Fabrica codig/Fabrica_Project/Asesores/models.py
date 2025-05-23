from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Presupuesto(models.Model):
    asesor = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    fecha_inicio = models.DateTimeField(null=False, auto_now_add=True, blank=False)
    cliente = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.TextField(null=False, blank=False)
    estado=models.TextField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)    
    
class Diseno(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.PROTECT, null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_cambio = models.DateTimeField(null=True, blank=True)
    estado=models.TextField(null=True, blank=True, default='Diseñando')
    comentario=models.TextField(null=True, blank=True)
    archivo = models.FileField( upload_to='media/disenosPresupuestos/',null=False, blank=False)