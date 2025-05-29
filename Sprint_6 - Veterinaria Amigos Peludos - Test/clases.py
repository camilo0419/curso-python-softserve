
class Mascota:
    '''La clase Mascota, representa a una mascota en el ejercicio de la clinica veterinaria.
    Sus atributos son: Nombre paciente, especie, raza, todos con tipo de dato Str, tambien,
    se añade a sus atributos un objeto dueno de la clase Dueno descrita en este mismo ejercico.
    Todos los atributos se almacenan en la lista consultas[]
    '''
    def __init__(self, nombre_paciente, especie, raza, dueno):
        '''El metodo constructor inicializa una nueva instancia de la clase Mascota con los argumentos
        nombre_paciente, especie, raza, dueno'''
        if not nombre_paciente.strip():
            raise ValueError("El nombre de la mascota no puede estar vacío.")
        self.nombre_paciente = nombre_paciente
        self.especie = especie
        self.raza = raza
        self.dueno = dueno
        self.consultas = []

    def informacion(self):
        '''Este metodo muestra la informacion basica de la mascota y su dueño'''
        print(f"Hola, me llamo {self.nombre_paciente}, soy un {self.especie}, de raza {self.raza} y mi tutor es {self.dueno.nombre_tutor}")

    def mostrar_historial(self):
        if not self.consultas:
            print(f"No hay consultas registradas para {self.nombre_paciente}.")
        else:
            print(f"\nHistorial de consultas de {self.nombre_paciente}:")
            for c in self.consultas:
                print(f" - {c}")
        '''Este metodo muestra la informacion relacionada con las consultas asociadas a la mascota'''

class Dueno:
    '''La clase Dueno, representa a un dueno en el ejercicio de la clinica veterinaria.
    Sus atributos son: nombre_tutor, telefono, direccion, todos con tipo de dato Str.
    '''
    def __init__(self, nombre_tutor, telefono, direccion):
        '''Metodo constructor que inicializa un objeto dueno de la clase Dueno con los argumentos:
        nombre_tutor, telefono, direccion'''
        if not telefono.isdigit() or len(telefono) < 10:
            raise ValueError("El teléfono debe contener solo dígitos y tener al menos 10 caracteres.")
        self.nombre_tutor = nombre_tutor
        self.telefono = telefono
        self.direccion = direccion

    def informacion(self):
        print(f"Soy {self.nombre_tutor}, Tel: {self.telefono}, Dirección: {self.direccion}")
        '''Metodo que muestra la informacion de un dueno de una mascota'''

class Consulta:
    '''La clase Consulta, representa una consulta en la veterinaria.
    Sus atributos son: fecha, motivo, diagnostico, todos de tipo Str.'''

    def __init__(self, fecha, motivo, diagnostico):
        '''Metodo constructor que inicializa un objeto consulta de la clase Consulta con los argumentos:
        fecha, motivo y diagnostico'''
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico

    def __str__(self):
        '''Representación en string de la consulta
        Returns:
            str: Información formateada de la consulta'''
        return f"{self.fecha} - Motivo: {self.motivo} | Diagnóstico: {self.diagnostico}"
