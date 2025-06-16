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
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='consultas')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.mascota.nombre_mascota} - {self.fecha}"
