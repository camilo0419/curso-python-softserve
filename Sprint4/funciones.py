from clases import Mascota, Dueno, Consulta

pacientes = []
tutores = []

def registrar_mascota():
    '''Resgitra una nueva mascota en el sistema junto con su tutor siguiendo el siguiente proceso:
    Se solicitan los datos de la mascota (nombre, especie, raza)
    Se solicitan los datos del tutor (nombre_tutor, telefono, direccion)
    Se crean los objetos de las clases Dueno y Mascota
    Se almacena la informacion en las listas tutores y pacientes'''
    print("\n--- Registrar Mascota ---")
    nombre = input("Nombre de la mascota: ")
    especie = input("Especie: ")
    raza = input("Raza: ")
    print("--- Datos del Tutor ---")
    nombre_tutor = input("Nombre del tutor: ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")

    dueno = Dueno(nombre_tutor, telefono, direccion)
    mascota = Mascota(nombre, especie, raza, dueno)

    tutores.append(dueno)
    pacientes.append(mascota)

    print(f"\n✅ Mascota '{nombre}' registrada con éxito.")

def registrar_consulta():
    '''Metodo que registra una consulta asociada a una mascota existente.
    El flujo es el siguiente:
    Se solicita el nombre de la mascota.
    Si la mascota existe, se procede a solicitar la informacion asociada a la consulta.
    Se crea y almacena la consulta asociada a la mascota.
    Si no existe, arroja una advertencia al usuario de que la mascota no existe
    '''
    print("\n--- Registrar Consulta ---")
    nombre = input("Nombre de la mascota: ")
    mascota = buscar_mascota(nombre)

    if mascota:
        fecha = input("Fecha de la consulta (dd/mm/aaaa): ")
        motivo = input("Motivo: ")
        diagnostico = input("Diagnóstico: ")

        nueva_consulta = Consulta(fecha, motivo, diagnostico)
        mascota.consultas.append(nueva_consulta)

        print(f"\n Consulta registrada para {mascota.nombre_paciente}.")
    else:
        print(f" Mascota '{nombre}' no encontrada.")

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
    nombre = input("Nombre de la mascota: ")
    mascota = buscar_mascota(nombre)

    if mascota:
        mascota.mostrar_historial()
    else:
        print(f"❌ Mascota '{nombre}' no encontrada.")

def buscar_mascota(nombre):
    '''Este metodo, busca una mascota por su nombbre, es case sensitive, por ello se anade .lower()
    para su ejecucion, debe proveerse el argumento tipo string nombre.
    El retorno en caso de encontrarlo es el objeto mascota o None en caso de que no haya nada '''
    for m in pacientes:
        if m.nombre_paciente.lower() == nombre.lower():
            return m
    return None
