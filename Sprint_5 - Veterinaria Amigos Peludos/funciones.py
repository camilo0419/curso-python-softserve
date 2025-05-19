from clases import Mascota, Dueno, Consulta
from logger import logger

pacientes = []
tutores = []

def registrar_mascota():
    '''Resgitra una nueva mascota en el sistema junto con su tutor siguiendo el siguiente proceso:
    Se solicitan los datos de la mascota (nombre, especie, raza)
    Se solicitan los datos del tutor (nombre_tutor, telefono, direccion)
    Se crean los objetos de las clases Dueno y Mascota
    Se almacena la informacion en las listas tutores y pacientes'''
    try:
        print("\n--- Registrar Mascota ---")
        nombre = input("Nombre de la mascota: ").strip()
        if not nombre:
            raise ValueError("El nombre de la mascota no puede estar vacío")
            #Valida que el nombre de la mascota no este en blanco.
        especie = input("Especie: ").strip()
        if not especie:
            raise ValueError("La especie no puede estar vacía")
            #Valida que la especie no este en blanco.
        raza = input("Raza: ").strip()
        if not raza:
            raise ValueError("La raza no puede estar vacía")
            #Valida que la raza no este vacia.

        print("--- Datos del Tutor ---")

        nombre_tutor = input("Nombre del tutor: ").strip()
        if not nombre_tutor:
            raise ValueError("El nombre del tutor no puede estar vacío")
            #Valida que el nombre del tutor no este vacio.
        telefono = input("Teléfono: ").strip()
        if not telefono.isdigit() or len(telefono) != 10:
            raise ValueError("El teléfono debe tener exactamente 10 dígitos numéricos.")
            #Valida que el número telefónico solo sean numeros y sean 10 digitos exactamente.
        direccion = input("Dirección: ").strip()
        if not direccion:
            raise ValueError("La direccion no puede estar vacía")
            #Valida que la dirección no este vacia.

        #if not all([nombre, especie, raza, nombre_tutor, telefono,direccion]):
        #   raise ValueError("Todos los campos deben ser completados.")  Valida que todos los campos no estuvieran vacios
        
        dueno = Dueno(nombre_tutor, telefono, direccion)
        mascota = Mascota(nombre, especie, raza, dueno)

        tutores.append(dueno)
        pacientes.append(mascota)

        logger.info(f"\nMascota '{nombre}' registrada con éxito.")
        #Registra en .log el registro exitoso
        print(f"\nMascota '{nombre}' registrada con éxito.")

    except ValueError as ve:
        logger.warning(f"Error al registrar mascota: {ve}")
        #Registra en .log si alguno de los datos estan incompletos.
        print(f" Error: {ve}")

    except Exception as e:
        logger.error(f"Error inesperado al registrar mascota: {e}")
        #Registra en .log si hay algun error inesperado.
        print(" Ocurrió un error inesperado.")

def registrar_consulta():
    '''Metodo que registra una consulta asociada a una mascota existente.
    El flujo es el siguiente:
    Se solicita el nombre de la mascota.
    Si la mascota existe, se procede a solicitar la informacion asociada a la consulta.
    Se crea y almacena la consulta asociada a la mascota.
    Si no existe, arroja una advertencia al usuario de que la mascota no existe
    '''
    print("\n--- Registrar Consulta ---")
    try:
        nombre = input("Nombre de la mascota: ")
        mascota = buscar_mascota(nombre)

        if  not mascota:
            raise LookupError(f"Mascota '{nombre}' no encontrada.")
            #Verifica si la mascota existe.

        fecha = input("Fecha de la consulta (dd/mm/aaaa): ").strip()
        motivo = input("Motivo: ").strip()
        diagnostico = input("Diagnóstico: ").strip()
        #Inputs de entrada

        if not all([fecha, motivo, diagnostico]):
            raise ValueError("Todos los campos de la consulta deben estar completos.")
            #Verifica el error si algun campo esta vacío.

        nueva_consulta = Consulta(fecha, motivo, diagnostico)
        mascota.consultas.append(nueva_consulta)

        logger.info(f"Consulta registrada para '{mascota.nombre_paciente}' el {fecha}.")
        #Log exitoso de la consulta con detalles
        print(f"\n Consulta registrada para {mascota.nombre_paciente}.")

    except LookupError as le:
        logger.warning(le)
        #Log de advartencia si la mascota no esta registrada.
        print(f"{le}")

    except ValueError as ve:
        logger.warning(f"Datos invalidos en la consulta: {ve}")
        #Log de advertencia para datos incompletos.
        print(f"Error: {ve}")

    except Exception as e:
        logger.error(f"Error inesperado al registrar consulta: {e}")
        #Log de error no previsto.
        print("Ocurrió un error inesperado.")

def listar_mascotas():
    '''Este metodo, muestra todas las mascotas registradas en el sistema.
    La informacion que arroja cuando se ejecuta es la siguiente:
    Los datos perteneciente a la mascota son: Nombre, especie, raza y datos del tutor.
    En caso de no encontrar mascotas nos da un aviso'''
    print("\n--- Lista de Mascotas ---")
    if not pacientes:
        print("No hay mascotas registradas.")
    else:
        for mascota in pacientes:
            mascota.informacion()

def ver_historial():
    '''Este metodo, muestra el historial completo de las consultas asociadas a una mascota especifica.
    El flujo es el siguiente:
    Busca la mascota por el nombre.
    Si existe, muestra todas las consultas asociadas a dicha mascota.
    Usa el metodo mostrar_historial() de la clase Mascota
    Imprime un aviso en caso de no encontrar a la mascota'''

    print("\n--- Historial de Consultas ---")
    try:
        nombre = input("Nombre de la mascota: ")
        mascota = buscar_mascota(nombre)

        if mascota:
            mascota.mostrar_historial()
        else:
            raise LookupError(f"Mascota '{nombre}' no encontrada.")
        
    except LookupError as le:
        print(le)

    except Exception as e:
        print("Ocurrio un error inesperado al mostrar el historial")

def buscar_mascota(nombre):
    '''Este metodo, busca una mascota por su nombbre, es case sensitive, por ello se anade .lower()
    para su ejecucion, debe proveerse el argumento tipo string nombre.
    El retorno en caso de encontrarlo es el objeto mascota o None en caso de que no haya nada '''
    for m in pacientes:
        if m.nombre_paciente.lower() == nombre.lower():
            return m
    return None