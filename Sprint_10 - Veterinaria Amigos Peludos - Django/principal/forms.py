from django import forms
from .models import Cliente, Mascota, Consulta

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


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre_mascota', 'especie', 'raza', 'edad', 'cliente']
        widgets = {
            'nombre_mascota': forms.TextInput(attrs={'placeholder': 'Nombre de la mascota'}),
            'especie': forms.TextInput(attrs={'placeholder': 'Especie'}),
            'raza': forms.TextInput(attrs={'placeholder': 'Raza'}),
            'edad': forms.NumberInput(attrs={'placeholder': 'Edad (en años)'}),
            'cliente': forms.Select(),
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['fecha', 'motivo', 'diagnostico', 'mascota']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'motivo': forms.Textarea(attrs={'placeholder': 'Motivo de la consulta'}),
            'diagnostico': forms.Textarea(attrs={'placeholder': 'Diagnóstico'}),
            'mascota': forms.Select(),
        }