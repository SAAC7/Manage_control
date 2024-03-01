from django import forms
from .models import Hoja_de_Produccion

class DisenoCNCForm(forms.Form):
    archivo = forms.FileField(label='Selecciona un archivo (PDF, RAR, JPG, PNG)', widget=forms.FileInput(attrs={'class': 'form-control cursor-pointer'}))

class DisenoProduccionForm(forms.Form):
    archivo = forms.FileField(label='Selecciona un archivo (PDF, RAR, JPG, PNG)', widget=forms.FileInput(attrs={'class': 'form-control cursor-pointer'}))
    
class HojaProduccionUpdateForm(forms.ModelForm):
    class Meta:
        model = Hoja_de_Produccion
        fields = ['diseno_CNC_id', 'diseno_produccion_id', 'estado']
