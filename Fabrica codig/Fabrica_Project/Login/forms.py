from django import forms
from django.contrib.auth.models import User, Group

class UserCreationForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre de usuario',widget=forms.TextInput(attrs={'class': 'form-control form-control-user'}),required=True)
    last_name = forms.CharField(label='Nombre de usuario',widget=forms.TextInput(attrs={'class': 'form-control form-control-user'}),required=True)
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-control form-control-user'}),required=True)
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control form-control-user'}),required=False)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user'}),required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Grupo', widget=forms.Select(attrs={'class': 'form-select'}),required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'group')
