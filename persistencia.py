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
    
def eliminar_dueno_logicamente_sqlite(dueno_id):
    """
    Realiza una eliminación lógica de un dueño, marcándolo como inactivo.

    Args:
        dueno_id (int): El ID del dueño a eliminar lógicamente.

    Returns:
        bool: True si el dueño fue marcado como inactivo con éxito, False en caso contrario.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        # Actualizamos la columna 'activo' a 0 para el dueño con el ID especificado
        cursor.execute("UPDATE duenos SET activo = 0 WHERE id = ?", (dueno_id,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas > 0 # Retorna True si se afectó al menos una fila
    except sqlite3.Error as e:
        print(f"Error al eliminar lógicamente el dueño: {e}")
        # Aquí podrías usar tu logger si lo tienes configurado para persistencia.py
        conexion.rollback()
        conexion.close()
        return False

def obtener_duenos_sqlite():
    """
    Obtiene todos los dueños ACTIVO de la base de datos.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_dueno FROM duenos WHERE activo = 1")
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
    cursor.execute("SELECT id, nombre_mascota FROM mascotas WHERE dueno_id = ? AND activo = 1", (dueno_id,))
    mascotas = cursor.fetchall()
    conexion.close()
    return mascotas

def obtener_consultas_con_id_sqlite(mascota_id):
    """
    Obtiene el historial de consultas activas para una mascota específica, incluyendo el ID de la consulta.

    Args:
        mascota_id (int): El ID de la mascota cuyas consultas se desean obtener.

    Returns:
        list: Una lista de tuplas, donde cada tupla contiene (id_consulta, fecha, motivo, diagnostico).
              Retorna una lista vacía si no hay consultas.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, fecha, motivo, diagnostico FROM consultas WHERE mascota_id = ? AND activo = 1", (mascota_id,))
    consultas = cursor.fetchall()
    conexion.close()
    return consultas

def actualizar_mascota_sqlite(mascota_id, nuevo_nombre = None, nueva_especie = None, nueva_raza = None, nueva_edad = None):
    """
    Actualiza los datos de una mascota existente.

    Args:
        mascota_id (int): El ID de la mascota a actualizar.
        nuevo_nombre (str, optional): Nuevo nombre de la mascota. Defaults to None.
        nueva_especie (str, optional): Nueva especie de la mascota. Defaults to None.
        nueva_raza (str, optional): Nueva raza de la mascota. Defaults to None.
        nueva_edad (int, optional): Nueva edad de la mascota. Defaults to None.

    Returns:
        bool: True si la mascota fue actualizada con éxito, False en caso contrario.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        campos_a_actualizar = []
        valores = []

        if nuevo_nombre is not None:
            campos_a_actualizar.append("nombre_mascota = ?")
            valores.append(nuevo_nombre)
        if nueva_especie is not None:
            campos_a_actualizar.append("especie = ?")
            valores.append(nueva_especie)
        if nueva_raza is not None:
            campos_a_actualizar.append("raza = ?")
            valores.append(nueva_raza)
        if nueva_edad is not None:
            campos_a_actualizar.append("edad = ?")
            valores.append(nueva_edad)

        if not campos_a_actualizar:
            conexion.close()
            return False #No hay campos a actualizar
        
        query = f"UPDATE mascotas SET {', '.join(campos_a_actualizar)} WHERE id = ?"
        valores.append(mascota_id)

        cursor.execute(query, tuple(valores))
        conexion.commit()
        filas_afectadas = cursor.rowcount 
        conexion.close()
        return filas_afectadas > 0
    except sqlite3.Error as e:
        print(f"Error al actualizar la mascota {e}")
        conexion.rollback()
        conexion.close()
        return False

def eliminar_mascota_logicamente_sqlite(mascota_id):
    """
    Realiza una eliminación lógica de una mascota, marcándola como inactiva.

    Args:
        mascota_id (int): El ID de la mascota a eliminar lógicamente.

    Returns:
        bool: True si la mascota fue marcada como inactiva con éxito, False en caso contrario.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("UPDATE mascotas SET activo = 0 WHERE id = ?", (mascota_id,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas > 0
    except sqlite3.Error as e:
        print(f"Error al eliminar lógicamente la mascota: {e}")
        conexion.rollback()
        conexion.close()
        return False

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
        WHERE mascota_id = ? AND activo = 1
        ORDER BY fecha DESC
    """, (mascota_id,))
    historial = cursor.fetchall()
    conexion.close()
    return historial

def actualizar_consulta_sqlite(consulta_id, nueva_fecha = None, nuevo_motivo = None, nuevo_diagnostico = None):
    """
    Actualiza los datos de una consulta existente.

    Args:
        consulta_id (int): El ID de la consulta a actualizar.
        nueva_fecha (str, optional): Nueva fecha de la consulta (YYYY-MM-DD). Defaults to None.
        nuevo_motivo (str, optional): Nuevo motivo de la consulta. Defaults to None.
        nuevo_diagnostico (str, optional): Nuevo diagnóstico de la consulta. Defaults to None.

    Returns:
        bool: True si la consulta fue actualizada con éxito, False en caso contrario.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        campos_a_actualizar = []
        valores = []

        if nueva_fecha is not None:
            campos_a_actualizar.append("fecha = ?")
            valores.append(nueva_fecha)
        if nuevo_motivo is not None:
            campos_a_actualizar.append("motivo = ?")
            valores.append(nuevo_motivo)
        if nuevo_diagnostico is not None:
            campos_a_actualizar.append("diagnostico = ?")
            valores.append(nuevo_diagnostico)

        if not campos_a_actualizar:
            conexion.close()
            return False # No hay consultas a actualizar
        
        query = f"UPDATE consultas SET {', '.join(campos_a_actualizar)} WHERE id = ?"
        valores.append(consulta_id)

        cursor.execute(query, tuple(valores))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas > 0
    except sqlite3.Error as e:
        print(f"Error al actualizar la consulta: {e}")
        conexion.rollback()
        conexion.close()
        return False

def eliminar_consulta_logicamente_sqlite(consulta_id):
    """
    Realiza una eliminación lógica de una consulta, marcándola como inactiva.

    Args:
        consulta_id (int): El ID de la consulta a eliminar lógicamente.

    Returns:
        bool: True si la consulta fue marcada como inactiva con éxito, False en caso contrario.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("UPDATE consultas SET activo = 0 WHERE id = ?", (consulta_id,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas > 0
    except sqlite3.Error as e:
        print(f"Error al eliminar lógicamente la consulta: {e}")
        conexion.rollback()
        conexion.close()
        return False