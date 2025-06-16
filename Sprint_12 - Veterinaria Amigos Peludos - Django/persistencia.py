import sqlite3
from conexion import crear_conexion

# --- Dueños ---

def registrar_dueno_sqlite(nombre, telefono, direccion):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO duenos (nombre_dueno, telefono, direccion) VALUES (?, ?, ?)",
                   (nombre, telefono, direccion))
    conexion.commit()
    conexion.close()

def actualizar_dueno_sqlite(dueno_id, nuevo_nombre = None, nuevo_telefono = None, nueva_direccion = None):
    """
    Actualiza los datos de un dueño existente en la base de datos SQLite.
    Permite actualizar uno o varios campos.

    Args:
        dueno_id (int): El ID del dueño a actualizar.
        nuevo_nombre (str, optional): El nuevo nombre del dueño. Si es None, no se actualiza.
        nuevo_telefono (str, optional): El nuevo teléfono del dueño. Si es None, no se actualiza.
        nueva_direccion (str, optional): La nueva dirección del dueño. Si es None, no se actualiza.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()

    # Construimos la consulta SQL dinámicamente
    # Esto es clave para actualizar solo los campos que se especifican
    updates = [] # Lista para guardar las partes 'campo = ?' de la consulta
    valores = [] # Lista para guardar los valores correspondientes a los campos

    if nuevo_nombre is not None:
        updates.append("nombre_dueno = ?")
        valores.append(nuevo_nombre)
    if nuevo_telefono is not None:
        updates.append("telefono = ?")
        valores.append(nuevo_telefono)
    if nueva_direccion is not None:
        updates.append("direccion = ?")
        valores.append(nueva_direccion)

    # Si no hay nada que actualizar (todos los campos son None), salimos
    if not updates:
        conexion.close()
        return False # Indicamos que no se realizó ninguna actualización

    # Unimos las partes de 'updates' con comas para formar el SET de la consulta
    query = f"UPDATE duenos SET {', '.join(updates)} WHERE id = ?"
    valores.append(dueno_id) # El ID siempre es el último valor para el WHERE

    try:
        cursor.execute(query, tuple(valores)) # Ejecutamos la consulta
        conexion.commit() # Guardamos los cambios
        filas_afectadas = cursor.rowcount # Esto nos dice cuántas filas se modificaron
        conexion.close()
        return filas_afectadas > 0 # Devolvemos True si se actualizó al menos una fila
    except sqlite3.Error as e:
        print(f"Error al actualizar dueño: {e}")
        conexion.rollback() # Deshacemos los cambios si hay un error
        conexion.close()
        return False

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
    
    mascotas = obtener_mascotas_por_dueno_sqlite(dueno_id)
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
