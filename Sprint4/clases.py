
class Mascota:
    def __init__(self, nombre_paciente, especie, raza, dueno):
        self.nombre_paciente = nombre_paciente
        self.especie = especie
        self.raza = raza
        self.dueno = dueno
        self.consultas = []

    def informacion(self):
        print(f"Hola, me llamo {self.nombre_paciente}, soy un {self.especie}, de raza {self.raza} y mi tutor es {self.dueno.nombre_tutor}")

    def mostrar_historial(self):
        if not self.consultas:
            print(f"No hay consultas registradas para {self.nombre_paciente}.")
        else:
            print(f"\nHistorial de consultas de {self.nombre_paciente}:")
            for c in self.consultas:
                print(f" - {c}")

class Dueno:
    def __init__(self, nombre_tutor, telefono, direccion):
        self.nombre_tutor = nombre_tutor
        self.telefono = telefono
        self.direccion = direccion

    def informacion(self):
        print(f"Soy {self.nombre_tutor}, Tel: {self.telefono}, Dirección: {self.direccion}")

class Consulta:
    def __init__(self, fecha, motivo, diagnostico):
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico

    def __str__(self):
        return f"{self.fecha} - Motivo: {self.motivo} | Diagnóstico: {self.diagnostico}"
