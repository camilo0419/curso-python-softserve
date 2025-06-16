import csv
import json
import os

from clases import Mascota, Dueno, Consulta
from logger import logger

pacientes = []
tutores = []

def guardar_datos(csv_path="Mascotas_dueños.csv", json_path="consultas.json"):
    try:
        with open(csv_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["nombre_mascota", "especie", "raza",
                                                   "nombre_tutor", "telefono", "direccion"])
            writer.writeheader()
            for m in pacientes:
                writer.writerow({
                    "nombre_mascota": m.nombre_paciente,
                    "especie": m.especie,
                    "raza": m.raza,
                    "nombre_tutor": m.dueno.nombre_tutor,
                    "telefono": m.dueno.telefono,
                    "direccion": m.dueno.direccion
                })
        logger.info(f"Datos de mascotas y dueños guardados en archivo CSV: {csv_path}.")        
        print(f"Datos de mascotas y dueños guardados en archivo CSV: {csv_path}.")

        data = {}
        for m in pacientes:
            consultas_mascota = []
            for c in m.consultas:
                consultas_mascota.append({
                    "fecha": c.fecha,
                    "motivo": c.motivo,
                    "diagnostico": c.diagnostico
                })
            data[m.nombre_paciente] = consultas_mascota

        with open(json_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logger.info(f"Datos de consultas guardados en archivo JSON: {json_path}.")
        print(f"Datos de consultas guardados en archivo JSON: {json_path}.")

    except Exception as e:
        logger.error(f"Error al guardar datos: {e}")
        print("Ocurrió un error al guardar los datos.")


def cargar_mascotas_duenos(csv_path="Mascotas_dueños.csv"):
    global pacientes, tutores
    try:
        if not os.path.exists(csv_path):
            logger.info(f"El archivo '{csv_path}' no existe. No se realiza ninguna carga")
            print(f"El archivo que intentas cargar no existe: {csv_path}")
            return
        
        with open(csv_path, "r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for fila_datos in reader:
                nombre_tutor = fila_datos["nombre_tutor"]
                telefono = fila_datos["telefono"]
                direccion = fila_datos["direccion"]
                dueno_existente = None
                for d in tutores:
                    if d.nombre_tutor == nombre_tutor and d.telefono == telefono:
                        dueno_existente = d
                        break
                if dueno_existente:
                    dueno = dueno_existente
                else:
                    dueno = Dueno(nombre_tutor, telefono, direccion)
                    tutores.append(dueno)
                
                nombre_mascota = fila_datos["nombre_mascota"]
                especie = fila_datos["especie"]
                raza = fila_datos["raza"]
                
                mascota = Mascota(nombre_mascota, especie, raza, dueno)
                pacientes.append(mascota)

        logger.info(f"Datos de mascotas y dueños cargados desde {csv_path}.") 
        print(f"Datos de mascotas y dueños cargados desde {csv_path}.")

    except FileNotFoundError:
        logger.error(f"Error: el archivo {csv_path} no fue encontrado")
        print(f"Error: el archivo {csv_path} no fue encontrado")
    except Exception as e:
        logger.error(f"Error al cargar los datos: {e}")
        print("Ocurrió un error inesperado al cargar los datos.")


def cargar_consultas(json_path="consultas.json"):
    global pacientes
    try:
        if not os.path.exists(json_path):
            logger.info(f"El archivo {json_path} no existe. No se realiza ninguna carga")
            print(f"El archivo {json_path} no fue encontrado. No se cargaron datos de consultas")
            return
        
        with open(json_path, "r", encoding='utf-8') as file:
            json_reader = json.load(file)
        
        for mascota_json, dict_json in json_reader.items():
            mascota_encontrada = None
            for p in pacientes:
                if p.nombre_paciente.lower() == mascota_json.lower():
                    mascota_encontrada = p
                    break
            if mascota_encontrada:
                for consulta_dict in dict_json:
                    fecha = consulta_dict["fecha"]
                    motivo = consulta_dict["motivo"]
                    diagnostico = consulta_dict["diagnostico"]

                    nueva_consulta = Consulta(fecha, motivo, diagnostico)
                    mascota_encontrada.consultas.append(nueva_consulta)
            else:
                logger.warning(f"Mascota '{mascota_json}' de JSON no encontrada en datos cargados. No se cargaron consultas")
                print(f"Advertencia, Mascota {mascota_json} no encontrada para cargar sus consultas")

        logger.info(f"Datos de consultas cargados exitosamente desde {json_path}.")
        print(f"Datos de consultas cargados exitosamente desde {json_path}.")

    except json.JSONDecodeError as jde:
        logger.error(f"Error al decodificar JSON desde {json_path}: {jde}.")
        print(f"Error: El archivo {json_path} tiene un formato JSON inválido. No se cargaron las consultas")
    except FileNotFoundError:
        logger.error(f"Error: El archivo {json_path} no fue encontrado durante la carga de JSON")
        print(f"Error: El archivo {json_path} no fue encontrado")
    except Exception as e:
        logger.error(f"Error inesperado al cargar datos JSON desde {json_path}: {e}.")
        print("Ocurrió un error inesperado al cargar los datos de consultas")



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