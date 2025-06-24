from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.cedula}"

class Mascota(models.Model):
    nombre_mascota = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, blank=True)
    raza = models.CharField(max_length=50, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas')
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return self.nombre_mascota

class Consulta(models.Model):
    fecha = models.DateField()
    motivo = models.TextField(blank=True)
    diagnostico = models.TextField(blank=True)
    tratamiento = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    req_medicamentos = models.BooleanField(default=False)
    req_cirugia = models.BooleanField(default=False) 
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='consultas')
    med_entregado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.mascota.nombre_mascota} - {self.fecha}"
    


class Medicamento(models.Model):
    nombre_med = models.CharField(max_length=100)
    presentacion = models.CharField(max_length=100)
    stock_disponible = models.IntegerField()
    fecha_vencimiento = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_med


class Profesional(models.Model):
    nombre_prof = models.CharField(max_length=100)
    tarjeta_profesional = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_prof

class Cirugia(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='cirugias')
    profesional = models.ForeignKey(Profesional, on_delete=models.SET_NULL, null=True, related_name='cirugias')
    procedimiento = models.CharField(max_length=255)
    descripcion_proced = models.TextField(blank=True, null=True)
    fecha_prog = models.DateField()
    hora_prog = models.TimeField()
    duracion_aprox = models.DurationField()
    estado = models.CharField(max_length=100)
    observaciones_cirugia = models.TextField(blank=True, null=True)
    # Relacion con Consulta
    # Esta relación es opcional, ya que no todas las cirugías están asociadas a una consulta
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='cirugia', null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.procedimiento} - {self.fecha_prog}"


class FormulaMedica(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='formulas')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='formulas')
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    via_administracion = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicamento.nombre_med} - {self.consulta}"
