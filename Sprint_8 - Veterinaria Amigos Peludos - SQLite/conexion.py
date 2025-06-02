import sqlite3

DB_NAME = "clinica_veterinaria.db"

def crear_conexion():
    conexion = sqlite3.connect(DB_NAME)
    conexion.execute("PRAGMA foreign_keys = ON")  # Habilitar claves foráneas
    return sqlite3.connect(DB_NAME)
    

def crear_tablas():
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duenos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_dueno TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_mascota TEXT NOT NULL,
            especie TEXT,
            raza TEXT,
            edad INTEGER,
            dueno_id INTEGER,
            FOREIGN KEY (dueno_id) REFERENCES duenos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            motivo TEXT,
            diagnostico TEXT,
            mascota_id INTEGER,
            FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
        )
    """)

    conexion.commit()
    conexion.close()
