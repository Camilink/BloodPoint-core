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
        widget=forms.EmailInput(attrs={'class':'form-control','disabled':'disabled'}),
        required=False
    )
    credencial = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class':'form-control'}),
        required=False,
        help_text="Sube tu credencial aquí"
    )

    class Meta:
        model = representante_org
        fields = ['nombre','apellido','rut_representante','rol']
        widgets = {
          'nombre': forms.TextInput(attrs={'class':'form-control'}),
          'apellido': forms.TextInput(attrs={'class':'form-control'}),
          'rut_representante': forms.TextInput(attrs={'class':'form-control'}),
          'rol': forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['email'].initial = self.instance.user.email