from clases import Mascota, Dueno, Consulta

pacientes = []
tutores = []

def registrar_mascota():
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
    print("\n--- Lista de Mascotas ---")
    if not pacientes:
        print("No hay mascotas registradas.")
    else:
        for mascota in pacientes:
            mascota.informacion()

def ver_historial():
    print("\n--- Historial de Consultas ---")
    nombre = input("Nombre de la mascota: ")
    mascota = buscar_mascota(nombre)

    if mascota:
        mascota.mostrar_historial()
    else:
        print(f"❌ Mascota '{nombre}' no encontrada.")

def buscar_mascota(nombre):
    for m in pacientes:
        if m.nombre_paciente.lower() == nombre.lower():
            return m
    return None
