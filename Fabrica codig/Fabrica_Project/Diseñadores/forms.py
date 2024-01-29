from django import forms

class DisenoForm(forms.Form):
    presupuesto_num = forms.IntegerField(label='Numero de presupuesto', widget=forms.TextInput(attrs={'class': 'form-control form-control-user'}), required=True)
    archivo = forms.FileField(label='Selecciona un archivo (PDF, RAR, JPG, PNG)', widget=forms.FileInput(attrs={'class': 'form-control cursor-pointer'}))
