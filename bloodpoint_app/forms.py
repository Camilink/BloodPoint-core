from django import forms
from .models import representante_org, adminbp
from cloudinary.forms import CloudinaryFileField

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
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        required=False 
    )

    class Meta:
        model = representante_org
        image = CloudinaryFileField(required=False)
        fields = ['nombre', 'apellido', 'rut_representante', 'rol', 'image']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut_representante': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['email'].initial = self.instance.user.email