from django import forms
# from Produccion.models import Hoja_de_Produccion

class PresupuestoForm(forms.Form):
    nombre_cliente = forms.CharField(label='Nombre del Cliente', widget=forms.TextInput(attrs={'class': 'form-control form-control-user'}), required=True)
    sol_design = forms.BooleanField(label='Mandar a Diseñar', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}))
    archivo = forms.FileField(label='Selecciona un archivo (PDF, RAR, JPG, PNG)', widget=forms.FileInput(attrs={'class': 'form-control cursor-pointer'}))
    descripcion = forms.CharField(label='Descripción', widget=forms.Textarea(attrs={'class': 'form-control form-control-user', 'rows': 7}), required=True)

class ContratoForm(forms.Form):
    presupuesto_num = forms.IntegerField(label='Numero de presupuesto', widget=forms.TextInput(attrs={'class': 'form-control form-control-user'}), required=True)
    contrato = forms.FileField(label='Selecciona un archivo (PDF, JPG, PNG)', widget=forms.FileInput(attrs={'class': 'form-control cursor-pointer'}))
    carta = forms.FileField(label='Selecciona un archivo (PDF, JPG, PNG)', widget=forms.FileInput(attrs={'class': 'form-control cursor-pointer'}))