from django import forms
from .models import Cliente, Mascota, Consulta, FormulaMedica, Medicamento, Profesional, Cirugia

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

PROCEDIMIENTOS_VETERINARIOS = [
    ('', 'Seleccione un procedimiento'),
    ('Castración', 'Castración'),
    ('Esterilización', 'Esterilización'),
    ('Extracción dental', 'Extracción dental'),
    ('Amputación', 'Amputación'),
    ('Apendicectomía', 'Apendicectomía'),
    ('Cesárea', 'Cesárea'),
    ('Limpieza de heridas', 'Limpieza de heridas'),
    ('Remoción de tumor', 'Remoción de tumor'),
    ('Laparotomía exploratoria', 'Laparotomía exploratoria'),
    ('Sutura de heridas', 'Sutura de heridas'),
]

DURACIONES = [
    ('00:30:00', '30 minutos'),
    ('01:00:00', '1 hora'),
    ('01:30:00', '1 hora 30 minutos'),
    ('02:00:00', '2 horas'),
    ('02:30:00', '2 horas 30 minutos'),
    ('03:00:00', '3 horas'),
    ('03:30:00', '3 horas 30 minutos'),
    ('04:00:00', '4 horas'),
    ('05:00:00', '5 horas'),
    ('06:00:00', '6 horas'),
]

class CirugiaForm(forms.ModelForm):
    procedimiento = forms.ChoiceField(choices=PROCEDIMIENTOS_VETERINARIOS)
    duracion_aprox = forms.ChoiceField(choices=DURACIONES)

    class Meta:
        model = Cirugia
        fields = [
            'procedimiento', 'descripcion_proced', 'fecha_prog',
            'hora_prog', 'duracion_aprox',
            'observaciones_cirugia', 'profesional'
        ]
        widgets = {
            'fecha_prog': forms.DateInput(attrs={'type': 'date'}),
            'hora_prog': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo establece valor inicial si no se está editando
        

