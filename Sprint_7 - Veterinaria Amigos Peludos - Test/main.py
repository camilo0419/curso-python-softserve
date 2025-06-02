from conexion import crear_tablas
from persistencia import (
    registrar_dueno_sqlite,
    obtener_duenos_sqlite,
    registrar_mascota_sqlite,
    obtener_mascotas_por_dueno_sqlite,
    registrar_consulta_sqlite,
    ver_historial_consultas_sqlite
)

def menu():
    crear_tablas()  #  Crear tablas desde el archivo conexion.py

    while True:
        print("\n--- Clínica Veterinaria ---")
        print("1. Registrar dueño")
        print("2. Registrar mascota")
        print("3. Listar dueños")
        print("4. Listar mascotas de un dueño")
        print("5. Registrar consulta")
        print("6. Ver historial de consultas de una mascota")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del dueño: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección: ")
            registrar_dueno_sqlite(nombre, telefono, direccion)
            print("Dueño registrado exitosamente.")

        elif opcion == "2":
            duenos = obtener_duenos_sqlite()
            if not duenos:
                print("No hay dueños registrados. Primero registre un dueño.")
                continue

            print("Dueños registrados:")
            for id_dueno, nombre_dueno in duenos:
                print(f"{id_dueno}: {nombre_dueno}")

            try:
                dueno_id = int(input("Ingrese el ID del dueño para la mascota: "))
                if dueno_id not in [d[0] for d in duenos]:
                    print("ID de dueño no válido.")
                    continue
            except ValueError:
                print("ID inválido.")
                continue

            nombre_mascota = input("Nombre de la mascota: ")
            especie = input("Especie: ")
            raza = input("Raza: ")
            try:
                edad = int(input("Edad: "))
            except ValueError:
                print("Edad inválida, debe ser un número.")
                continue

            registrar_mascota_sqlite(nombre_mascota, especie, raza, edad, dueno_id)
            print("Mascota registrada exitosamente.")

        elif opcion == "3":
            duenos = obtener_duenos_sqlite()
            if not duenos:
                print("No hay dueños registrados.")
            else:
                print("Dueños registrados:")
                for id_dueno, nombre_dueno in duenos:
                    print(f"{id_dueno}: {nombre_dueno}")

        elif opcion == "4":
            try:
                dueno_id = int(input("Ingrese el ID del dueño: "))
            except ValueError:
                print("ID inválido.")
                continue

            mascotas = obtener_mascotas_por_dueno_sqlite(dueno_id)
            if not mascotas:
                print("No se encontraron mascotas para ese dueño.")
            else:
                print("Mascotas registradas:")
                for id_mascota, nombre_mascota in mascotas:
                    print(f"{id_mascota}: {nombre_mascota}")

        elif opcion == "5":
            # Obtener todas las mascotas
            duenos = obtener_duenos_sqlite()
            if not duenos:
                print("No hay dueños ni mascotas registrados.")
                continue

            print("Dueños registrados:")
            for id_dueno, nombre_dueno in duenos:
                print(f"{id_dueno}: {nombre_dueno}")

            try:
                dueno_id = int(input("Ingrese el ID del dueño para ver sus mascotas: "))
            except ValueError:
                print("ID inválido.")
                continue

            mascotas = obtener_mascotas_por_dueno_sqlite(dueno_id)
            if not mascotas:
                print("Este dueño no tiene mascotas registradas.")
                continue

            print("Mascotas del dueño:")
            for id_mascota, nombre_mascota in mascotas:
                print(f"{id_mascota}: {nombre_mascota}")

            try:
                mascota_id = int(input("Ingrese el ID de la mascota para registrar la consulta: "))
                if mascota_id not in [m[0] for m in mascotas]:
                    print("ID de mascota no válido.")
                    continue
            except ValueError:
                print("ID inválido.")
                continue

            fecha = input("Fecha (YYYY-MM-DD): ")
            motivo = input("Motivo de la consulta: ")
            diagnostico = input("Diagnóstico: ")

            registrar_consulta_sqlite(fecha, motivo, diagnostico, mascota_id)
            print("Consulta registrada exitosamente.")


        elif opcion == "6":
            try:
                mascota_id = int(input("ID de la mascota: "))
            except ValueError:
                print("ID inválido.")
                continue

            historial = ver_historial_consultas_sqlite(mascota_id)
            if not historial:
                print("No se encontró historial para esa mascota.")
            else:
                print("Historial de consultas:")
                for fecha, motivo, diagnostico in historial:
                    print(f"{fecha} - {motivo}: {diagnostico}")

        elif opcion == "7":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
