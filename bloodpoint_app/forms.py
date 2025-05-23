from django import forms
from .models import representante_org, adminbp

class RepresentanteOrgForm(forms.ModelForm):
    class Meta:
        model = representante_org
        fields = ['user', 'rol', 'nombre']
        widgets = {
            'rol': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }


class AdminBPForm(forms.ModelForm):
    class Meta:
        model = adminbp
        fields = ['nombre', 'email', 'contrasena']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
