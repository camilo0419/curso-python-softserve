from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'cedula', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Cédula'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if Cliente.objects.filter(cedula=cedula, activo=True).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un cliente con esta cédula.")
        return cedula
