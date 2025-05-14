from funciones import registrar_mascota, registrar_consulta, listar_mascotas, ver_historial

def menu():
    while True:
        print("\n--- Clínica Veterinaria Amigos Peludos ---")
        print("1. Registrar Mascota")
        print("2. Registrar Consulta")
        print("3. Listar Mascotas")
        print("4. Ver Historial de Consultas")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_mascota()
        elif opcion == "2":
            registrar_consulta()
        elif opcion == "3":
            listar_mascotas()
        elif opcion == "4":
            ver_historial()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
