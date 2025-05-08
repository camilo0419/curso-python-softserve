import re

def crear_correo():
    estudiante_patron = r"^[a-z0-9_.+-]+@estudiante\.utv\.edu\.co$"
    docente_patron = r"^[a-z0-9_.+-]+@utv\.edu\.co$"

    while True:
        correo = input("Por favor ingrese su correo electrónico de la universidad: ").strip().lower()

        if " " in correo:
            print("El correo no debe contener espacios.")
        elif re.match(estudiante_patron, correo):
            print(f"Correo válido registrado: {correo}")
            return correo, "estudiante"
        elif re.match(docente_patron, correo):
            print(f"Correo válido registrado: {correo}")
            return correo, "docente"
        else:
            print("Correo inválido. Debe ingresar un correo de la universidad.")       

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
