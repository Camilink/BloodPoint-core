from django import forms
from .models import representante_org, adminbp

class AdminBPForm(forms.ModelForm):
    class Meta:
        model = adminbp
        fields = ['nombre', 'email', 'contrasena']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class RepresentanteOrgForm(forms.ModelForm):
    class Meta:
        model = representante_org
        fields = ['nombre', 'apellido', 'rut_representante', 'rol', 'credencial']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut_representante': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.TextInput(attrs={'class': 'form-control'}),
            'credencial': forms.FileInput(attrs={'class': 'form-control'}),
        }
