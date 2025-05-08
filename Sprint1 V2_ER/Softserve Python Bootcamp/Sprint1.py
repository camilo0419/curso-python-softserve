import funciones 
Personal = {}

while True:
    print("\nBienvenido a la Universidad Tecnológica del Valle\n")
    print("Menu principal")
    print("(1) Registrar nuevo correo")
    print("(2) Ver correos registrados")
    print("(3) Buscar un correo específico")
    print("(4) Salir\n")
    opcion = input("Seleccione una opción del menú principal: ").strip()

    if opcion == "1":
        correo, tipo = funciones.crear_correo()
        if correo:
            Personal[correo] = tipo
    #Guarda en Personal el correo y el tipo.        
    elif opcion == "2":
        if Personal:
        #Verifica si existen registros
            print("\nCorreos registrados:")
            for correo, tipo in Personal.items():
            #Ciclo para cada registro en Personal
                print(f"{correo} ({tipo})")
                #Muestra Personal con el correo y el tipo.
        else:
            print("No hay correos registrados.")

    elif opcion == "3":
        busqueda = input("Ingrese palabra clave que desea buscar: ")
        # Recogemos los caracteres que se quieren buscar.
        funciones.buscar(Personal, busqueda)
        

    elif opcion == "4":
        print("Gracias por usar nuestro sistema. ¡Hasta pronto!")
        break
    else:
        print("La opción ingresada no es válida, por favor intente de nuevo.")
