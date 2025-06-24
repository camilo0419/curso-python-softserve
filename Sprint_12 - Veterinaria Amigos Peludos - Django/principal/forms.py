from django import forms
from .models import Cliente, Mascota, Consulta, FormulaMedica, Medicamento, Profesional

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
        fields = [
            'fecha', 
            'motivo', 
            'diagnostico', 
            'mascota',
            'tratamiento',
            'observaciones',
            'req_medicamentos',
            'req_cirugia'
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'motivo': forms.Textarea(attrs={'placeholder': 'Motivo de la consulta'}),
            'diagnostico': forms.Textarea(attrs={'placeholder': 'Diagnóstico'}),
            'mascota': forms.Select(),
            'tratamiento': forms.Textarea(attrs={'placeholder': 'Tratamiento prescrito'}),
            'observaciones': forms.Textarea(attrs={'placeholder': 'Observaciones adicionales'}),
        }

class FormulaMedicaForm(forms.ModelForm):
    class Meta:
        model = FormulaMedica
        fields = [
            'medicamento', 'dosis', 'frecuencia', 
            'duracion', 'via_administracion', 'observaciones'
        ]
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1 tableta'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: cada 8 horas'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 5 días'}),
            'via_administracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Oral'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
        }
class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre_med', 'presentacion', 'stock_disponible', 'fecha_vencimiento']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'nombre_med': forms.TextInput(attrs={'placeholder': 'Nombre del medicamento'}),
            'presentacion': forms.TextInput(attrs={'placeholder': 'Ej: Tableta, Inyectable...'}),
        }


class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['nombre_prof', 'tarjeta_profesional', 'telefono', 'especialidad', 'activo']
        widgets = {
            'nombre_prof': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'tarjeta_profesional': forms.TextInput(attrs={'placeholder': 'Número de tarjeta'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: 3201234567'}),
            'especialidad': forms.TextInput(attrs={'placeholder': 'Ej: Cirujano, General'}),
        }
