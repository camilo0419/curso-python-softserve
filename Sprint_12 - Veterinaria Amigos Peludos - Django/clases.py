
class Mascota:
    '''La clase Mascota, representa a una mascota en el ejercicio de la clinica veterinaria.
    Sus atributos son: Nombre mascota, especie, raza, todos con tipo de dato Str, tambien,
    se añade a sus atributos un objeto dueno de la clase Dueno descrita en este mismo ejercico.
    Todos los atributos se almacenan en la lista consultas[]
    '''
    def __init__(self, nombre_mascota, especie, raza, edad, dueno_id, id=None):
        '''El metodo constructor inicializa una nueva instancia de la clase Mascota con los argumentos
        nombre_mascota, especie, raza, dueno'''
        if not nombre_mascota.strip():
            raise ValueError("El nombre de la mascota no puede estar vacío.")
        self.id = id
        self.nombre_mascota = nombre_mascota
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.dueno_id = dueno_id
        self.consultas = []

    def informacion(self):
        '''Este metodo muestra la informacion basica de la mascota y su dueño'''
        print(f"Hola, me llamo {self.nombre_mascota}, soy un {self.especie}, de raza {self.raza} y mi tutor es {self.dueno.nombre_dueno}")

    def mostrar_historial(self):
        if not self.consultas:
            print(f"No hay consultas registradas para {self.nombre_mascota}.")
        else:
            print(f"\nHistorial de consultas de {self.nombre_mascota}:")
            for c in self.consultas:
                print(f" - {c}")
        '''Este metodo muestra la informacion relacionada con las consultas asociadas a la mascota'''

class Dueno:
    '''La clase Dueno, representa a un dueno en el ejercicio de la clinica veterinaria.
    Sus atributos son: nombre_dueno, telefono, direccion, todos con tipo de dato Str.
    '''
    def __init__(self, nombre_dueno, telefono, direccion, id=None):
        '''Metodo constructor que inicializa un objeto dueno de la clase Dueno con los argumentos:
        nombre_dueno, telefono, direccion'''
        if not telefono.isdigit() or len(telefono) < 10:
            raise ValueError("El teléfono debe contener solo dígitos y tener al menos 10 caracteres.")
        self.id = id
        self.nombre_dueno = nombre_dueno
        self.telefono = telefono
        self.direccion = direccion

    def informacion(self):
        print(f"Soy {self.nombre_dueno}, Tel: {self.telefono}, Dirección: {self.direccion}")
        '''Metodo que muestra la informacion de un dueno de una mascota'''

class Consulta:
    '''La clase Consulta, representa una consulta en la veterinaria.
    Sus atributos son: fecha, motivo, diagnostico, todos de tipo Str.'''

    def __init__(self, fecha, motivo, diagnostico, mascota_id, id=None):
        '''Metodo constructor que inicializa un objeto consulta de la clase Consulta con los argumentos:
        fecha, motivo y diagnostico'''
        self.id = id
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota_id = mascota_id

    def __str__(self):
        '''Representación en string de la consulta
        Returns:
            str: Información formateada de la consulta'''
        return f"{self.fecha} - Motivo: {self.motivo} | Diagnóstico: {self.diagnostico}"
