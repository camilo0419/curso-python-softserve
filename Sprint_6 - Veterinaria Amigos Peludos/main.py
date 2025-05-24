from funciones import (
    registrar_mascota,
    registrar_consulta,
    listar_mascotas,
    ver_historial,
    guardar_datos,
    cargar_datos,
    cargar_consultas
)
from logger import logger

def menu():
    logger.info("Inicio de la Aplicación")
    #Registra el inicio de la aplicaión en clinica_veterinaria.log
    cargar_datos("Mascotas_dueños.csv")
    cargar_consultas("consultas.json")
    while True:
        print("\n--- Clínica Veterinaria Amigos Peludos ---")
        print("1. Registrar Mascota")
        print("2. Registrar Consulta")
        print("3. Listar Mascotas")
        print("4. Ver Historial de Consultas")
        print("5. Guardar")
        print("6. Salir y guardar")

        opcion = input("Seleccione una opción: ")

        try:

            if opcion == "1":
                registrar_mascota()
            elif opcion == "2":
                registrar_consulta()
            elif opcion == "3":
                listar_mascotas()
            elif opcion == "4":
                ver_historial()
            elif opcion == "5":
                guardar_datos()
            elif opcion == "6":
                guardar_datos()
                print("¡Hasta luego!")
                logger.info("Cierre de la aplicación")
                #Registra el cierre de la Aplicación en el logging
                break
            else:
                raise ValueError("Opción no válida.")
            
        except ValueError as ve:
            logger.warning(f"Opción inválida seleccionada: {opcion}")
            #Registra en .log la entrada invalida
            print(f"{ve}")

if __name__ == "__main__":
    menu()
