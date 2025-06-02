from conexion import crear_conexion

# --- Dueños ---

def registrar_dueno_sqlite(nombre, telefono, direccion):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO duenos (nombre_dueno, telefono, direccion) VALUES (?, ?, ?)",
                   (nombre, telefono, direccion))
    conexion.commit()
    conexion.close()

def obtener_duenos_sqlite():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_dueno FROM duenos")
    duenos = cursor.fetchall()
    conexion.close()
    return duenos

# --- Mascotas ---

def registrar_mascota_sqlite(nombre, especie, raza, edad, dueno_id):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO mascotas (nombre_mascota, especie, raza, edad, dueno_id)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, especie, raza, edad, dueno_id))
    conexion.commit()
    conexion.close()
    


def obtener_mascotas_por_dueno_sqlite(dueno_id):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_mascota FROM mascotas WHERE dueno_id = ?", (dueno_id,))
    mascotas = cursor.fetchall()
    conexion.close()
    return mascotas

def listar_mascotas():
    try:
        dueno_id = int(input("Ingrese el ID del dueño para listar sus mascotas: "))
    except ValueError:
        print("ID inválido.")
        return
    
    mascotas = obtener_mascotas_por_dueno(dueno_id)
    if not mascotas:
        print("No se encontraron mascotas para ese dueño.")
        return
    
    print(f"Mascotas del dueño {dueno_id}:")
    for id_mascota, nombre_mascota in mascotas:
        print(f"{id_mascota}: {nombre_mascota}")



# --- Consultas ---

def registrar_consulta_sqlite(fecha, motivo, diagnostico, mascota_id):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO consultas (fecha, motivo, diagnostico, mascota_id)
        VALUES (?, ?, ?, ?)
    """, (fecha, motivo, diagnostico, mascota_id))
    conexion.commit()
    conexion.close()

def ver_historial_consultas_sqlite(mascota_id):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT fecha, motivo, diagnostico FROM consultas
        WHERE mascota_id = ?
        ORDER BY fecha DESC
    """, (mascota_id,))
    historial = cursor.fetchall()
    conexion.close()
    return historial
