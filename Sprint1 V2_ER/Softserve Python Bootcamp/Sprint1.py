import funciones 
Personal = {}

while True:

# Por medio de un bucle while infinito se recorren las opciones del menu, finalizando con break en la opcion 4 
    
    print("\nBienvenido a la Universidad Tecnológica del Valle\n")
    print("Menu principal")
    print("(1) Registrar nuevo correo")
    print("(2) Ver correos registrados")
    print("(3) Buscar un correo específico")
    print("(4) Salir\n")
    opcion = input("Seleccione una opción del menú principal: ").strip()

# El metodo strip() nos permite almacenar informacion limpia sin espacios al inicio o al final para evitar errores innecesarios
    
    if opcion == "1":
        correo, tipo = funciones.crear_correo()
        if correo:
            Personal[correo] = tipo

# Se invoca a la funcion crear_correo() la cual solicita almacena los datos en el diccionario 'Personal{}' siendo el correo registrado
# la 'clave' y el tipo de rol el 'valor'
    
    elif opcion == "2":
        if Personal:        
            print("\nCorreos registrados:")
            for correo, tipo in Personal.items():
                print(f"{correo} ({tipo})")
        else:
            print("No hay correos registrados.")

# Se ejecuta una verificacion del diccionario 'Personal{}' confirmando que no este vacio, por medio de un ciclo for, iteramos con los valores
# 'correo' y 'tipo' para finalmente imprimir cada item con su respectiva 'clave' y 'valor'

    elif opcion == "3":
        busqueda = input("Ingrese palabra clave que desea buscar: ")
        funciones.buscar(Personal, busqueda)
        
# Inicialmente se recibe una cadena de caracteres para iniciar la busqueda, luego se invoca la funcion buscar(diccionario, busqueda) con sus 
# respectivos parametros. Una vez obtenidos los parametros la funcion ejecutara una busqueda en el diccionario, mostrando solo los correos que
# contengan la informacion almacenada en la variable 'busqueda'

    elif opcion == "4":
        print("Gracias por usar nuestro sistema. ¡Hasta pronto!")
        break
    else:
        print("La opción ingresada no es válida, por favor intente de nuevo.")

# Finaliza el bucle por medio de la instruccion break, en caso de opciones que no obedezcan a la condicion Int o esten en el rango de 1 - 4,
# se consideraran entradas invalidas, reiniciando el bucle. 
