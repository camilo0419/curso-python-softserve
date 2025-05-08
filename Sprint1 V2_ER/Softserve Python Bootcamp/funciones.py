import re

def crear_correo():
    estudiante_patron = r"^[a-z0-9_.+-]+@estudiante\.utv\.edu\.co$"
    #Asignamos el patron permitido para estudiante.
    docente_patron = r"^[a-z0-9_.+-]+@utv\.edu\.co$"
    #Asigmanos el patron permitido para docente.

    while True:
        correo = input("Por favor ingrese su correo electrónico de la universidad: ").strip().lower()
        #Recogemos el correo del usuario, reliminando espacios y pasando a minuscula.

        if " " in correo:
            print("El correo no debe contener espacios.")
            #Valida que el correo ingresado no contenga espacios.
        elif re.match(estudiante_patron, correo):
            #Validamos que el correo ingresado sea de estudiante.
            print(f"Correo registrado exitosamente: {correo}")
            return correo, "Estudiante"
            #Retornamos a Personal{} el correo y el tipo Estudiante.
        elif re.match(docente_patron, correo):
            print(f"Correo registrado exitosamente: {correo}")
            #Validamos que el correo ingresado sea de docente.
            return correo, "Docente"
            #Retornamos a Personal{} el correo y el tipo Docente.
        else:
            print("Correo inválido. Debe ingresar un correo de la universidad.")
            #Si no se cumple ninguna de las anteriores, debe ingresar nuevamente el correo.       


def buscar(diccionario, busqueda):
    # Asignamos los parámetros de la función.
    busqueda = busqueda.strip().lower()
    # Eliminamos y pasamos a minúsculas los caracteres por buscar.
    encontrados = []
    # Creamos una lista con lo que se va a encontrar.

    patron = re.compile(busqueda)
    # Compilamos la búsqueda ingresada por el usuario para usarse en la búsqueda.

    for correo, tipo in diccionario.items():
        # Recorre diccionario
        # Buscamos si la búsqueda está en el correo o en el tipo.
        if patron.search(correo) or patron.search(tipo.lower()):
            encontrados.append((correo, tipo))
            # Agrega a encontrados[] los elementos que coinciden con la busqueda.

    if encontrados:
        # Verifica si hay almenos una coincidencia
        print("\nCoincidencias encontradas:")
        for correo, tipo in encontrados:
            print(f"- {correo} ({tipo})")
            # Muestra los item encontrados.
    else:
        print("No se encontraron coincidencias.")

