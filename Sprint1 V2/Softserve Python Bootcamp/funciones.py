

def crear_correo():
    while True:
        correo = input("Por favor ingrese su correo electrónico de la universidad: ").strip().lower()
        #Bucle hasta que ingrese un correo váido

        if " " in correo:
            print("El correo no debe contener espacios.")
            #Verifica que el correo ingresado no tenga espacios.
        elif correo.endswith("@estudiante.utv.edu.co"):
            print(f"Correo válido registrado: {correo}")
            return correo, "estudiante"
            #Verifica si el correo ingresado finaliza con el dominio de estudiante y retorna correo y tipo
        elif correo.endswith("@utv.edu.co"):
            print(f"Correo válido registrado: {correo}")
            return correo, "docente"
            #Verifica si el correo ingresado finaliza con el dominio de docente y retorna correo y tipo
        
        else:
            print("Correo inválido. Debe ingresar un correo de la universidad.")
            #Devuelve el mensaje de Ínvalido si no cumple con los dos tipos o finaliza con otro dominio.

            

def buscar(diccionario, busqueda):
    busqueda = busqueda.strip().lower()
    encontrados = []

    for correo, tipo in diccionario.items():
        if busqueda in correo:
            encontrados.append((correo, tipo))

    if encontrados:
        print("\nCoincidencias encontradas:")
        for correo, tipo in encontrados:
            print(f"- {correo} ({tipo})")
    else:
        print("No se encontraron coincidencias.")
