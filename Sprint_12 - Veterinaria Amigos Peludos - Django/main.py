from conexion import crear_tablas
from logger import logger
from persistencia import (
    registrar_dueno_sqlite,
    obtener_duenos_sqlite,
    registrar_mascota_sqlite,
    obtener_mascotas_por_dueno_sqlite,
    registrar_consulta_sqlite,
    ver_historial_consultas_sqlite,
    actualizar_dueno_sqlite
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
        print("7. Actualizar datos dueño")
        print("8. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            try:
                nombre = input("\nNombre del dueño: ").strip()
                if not nombre.isalpha():
                    raise ValueError("\nError! El nombre del dueño no puede estar vacio y solo debe contener solo letras")
                telefono = input("Teléfono: ").strip()
                if not telefono.isdigit():
                    raise ValueError("\nError! El telefono del dueño no puede estar vacio y solo debe contener numeros")
                direccion = input("Dirección: ").strip()
                if not direccion:
                    raise ValueError("\nError! La direccion del dueño no puede estar vacia")
                registrar_dueno_sqlite(nombre, telefono, direccion)
                logger.info(f"Dueño: {nombre}, Telefono: {telefono}, Direccion: {direccion}, registrados satisfactoriamente")
                print("\nDueño registrado exitosamente.")                
            except ValueError as CharError:
                logger.info("Proceso de registro de Dueño no se pudo completar debido a un error en los parametros requeridos")
                print(f"{CharError}")

        elif opcion == "2":
            duenos = obtener_duenos_sqlite()
            if not duenos:
                logger.info("Proceso de obtencion de Dueño en base de datos no se pudo completar, no existen registros asociados")
                print("\nNo hay dueños registrados. Primero registre un dueño.")
                continue

            print("\nDueños registrados:")
            for id_dueno, nombre_dueno in duenos:
                logger.info("Proceso obtencion de Dueños alojados en la base de datos, completado con exito")
                print(f"{id_dueno}: {nombre_dueno}")

            try:
                dueno_id = int(input("\nIngrese el ID del dueño para la mascota: "))
                if dueno_id not in [d[0] for d in duenos]:
                    print("\nID de dueño no válido.")
                    continue
            except ValueError:
                logger.info(f"El ID: {dueno_id} no se encuentra asociado a ningun registro en la base de datos ")
                print("\nID inválido.")
                continue

            try:
                nombre_mascota = input("\nNombre de la mascota: ").strip()
                if not nombre_mascota.isalpha():
                    raise ValueError("\nError! El nombre no puede estar vacio y solo debe contener solo letras")
                especie = input("Especie: ").strip()
                if not especie.isalpha():
                    raise ValueError("\nError! La especie no puede estar vacio y solo debe contener solo letras")
                raza = input("Raza: ").strip()
                if not raza.isalpha():
                    raise ValueError("\nError! La raza no puede estar vacio y solo debe contener solo letras")
            except ValueError as CharError:
                logger.info("Proceso de registro de Mascota no se pudo completar debido a un error en los parametros requeridos")
                print(f"\n{CharError}")
                continue
            
            try:
                edad = int(input("Edad: "))
            except ValueError:
                logger.info("Proceso de registro de Mascota no se pudo completar debido a un error en los parametros requeridos")
                print("\nEdad inválida, debe ser un número.")
                continue

            registrar_mascota_sqlite(nombre_mascota, especie, raza, edad, dueno_id)
            logger.info("Proceso de registro de Mascota completado satisfactoriamente")
            print("\nMascota registrada exitosamente.")

        elif opcion == "3":
            duenos = obtener_duenos_sqlite()
            if not duenos:
                logger.info("Proceso de obtencion de Dueño en base de datos no se pudo completar, no existen registros asociados")
                print("\nNo hay dueños registrados.")
            else:
                print("\nDueños registrados:")
                for id_dueno, nombre_dueno in duenos:
                    logger.info("Proceso de Listar Dueños existentes en base de datos completado con exito")
                    print(f"{id_dueno}: {nombre_dueno}")

        elif opcion == "4":

            duenos = obtener_duenos_sqlite()
            if not duenos:
                logger.info("Proceso de obtencion de Dueño en base de datos no se pudo completar, no existen registros asociados")
                print("\nNo hay dueños registrados.")
            print("\nDueños registrados:")
            for id_dueno, nombre_dueno in duenos:
                logger.info("Proceso de Listar Dueños existentes en base de datos completado con exito")
                print(f"{id_dueno}: {nombre_dueno}")

            try:                
                dueno_id = int(input("\nIngrese el ID del dueño: ").strip())
                if not dueno_id:
                    raise ValueError("\nError! Este campo no puede estar vacio y debe ser un numero")
            except ValueError as ID_Selection_Error:
                logger.info("Proceso de listar Mascotas por ID no se pudo completar debido a un error en los parametros requeridos")
                print(f"\n{ID_Selection_Error}")
                continue

            mascotas = obtener_mascotas_por_dueno_sqlite(dueno_id)
            if not mascotas:
                logger.info("Proceso de obtencion de Mascotas asociadas a ID dueño existentes en base de datos no se pudo completar, no existen registros asociados")
                print("\nNo se encontraron mascotas para ese dueño.")
            else:
                print("\nMascotas registradas:")
                for id_mascota, nombre_mascota in mascotas:
                    logger.info("Proceso de Listar Mascotas asociadas a Dueños existentes en base de datos completado con exito")
                    print(f"{id_mascota}: {nombre_mascota}")

        elif opcion == "5":
            # Obtener todas las mascotas
            duenos = obtener_duenos_sqlite()
            if not duenos:
                logger.info("Proceso de obtencion de Dueño en base de datos no se pudo completar, no existen registros asociados")
                print("\nNo hay dueños ni mascotas registrados.")
                continue

            print("\nDueños registrados:")
            for id_dueno, nombre_dueno in duenos:
                logger.info("Proceso de Listar Dueños existentes en base de datos completado con exito")
                print(f"{id_dueno}: {nombre_dueno}")
            
            try:
                dueno_id = input("\nIngrese el ID del dueño para ver sus mascotas: ")
                if not dueno_id.strip():
                    raise ValueError("Error! Este campo no puede estar vacio")
                else:
                    int(dueno_id)
            except ValueError as EmptyFieldError:
                logger.info("Proceso de listar Dueños por ID no se pudo completar debido a un error en los parametros requeridos")
                print(f"\n{EmptyFieldError}")
                continue

            mascotas = obtener_mascotas_por_dueno_sqlite(dueno_id)
            if not mascotas:
                logger.info(f"Proceso de Obtener Mascotas asociadas a ID Dueño no se pudo completar, no hay registros asociados a {dueno_id}")
                print("\nEste dueño no tiene mascotas registradas.")
                continue

            print("\nMascotas del dueño:")
            for id_mascota, nombre_mascota in mascotas:
                logger.info("Proceso de Listar Mascotas existentes en base de datos completado con exito")
                print(f"{id_mascota}: {nombre_mascota}")
            
            try:
                mascota_id = int(input("\nIngrese el ID de la mascota para registrar la consulta: "))
                if mascota_id not in [m[0] for m in mascotas]:
                    logger.info(f"El ID: {mascota_id} no se encuentra asociado a ningun registro en la base de datos ")
                    print("\nID de mascota no válido.")
                    continue
            except ValueError:
                logger.info(f"Proceso de listar Mascotas asociadas a ID Dueño no se pudo completar no hay registros asociados a {mascota_id}")
                print("\nID inválido.")
                continue

            try:

                fecha = input("\nFecha (YYYY-MM-DD): ").strip()
                if not fecha:
                    raise ValueError("Error! La fecha no puede estar vacia")
                motivo = input("Motivo de la consulta: ").strip()
                if not motivo:
                    raise ValueError("Error! Este campo no debe estar vacio")
                diagnostico = input("Diagnóstico: ").strip()
                if not diagnostico:
                    raise ValueError("Error! Este campo no debe estar vacio")
            except ValueError as TypingError:
                logger.info("Proceso de Registrar Consulta de una Mascota por ID, no se pudo completar debido a un error en los parametros requeridos")
                print(f"{TypingError}")
                continue

            registrar_consulta_sqlite(fecha, motivo, diagnostico, mascota_id)
            logger.info("Proceso de Registrar Consulta de una Mascota por ID, completado satisfactoriamente")
            print("\nConsulta registrada exitosamente.")


        elif opcion == "6":
            
            duenos = obtener_duenos_sqlite()
            if not duenos:
                logger.info("Proceso de obtencion de Dueño en base de datos no se pudo completar, no existen registros asociados")
                print("\nNo hay dueños ni mascotas registrados.")
                continue

            print("\nDueños registrados:")
            for id_dueno, nombre_dueno in duenos:
                logger.info("Proceso de Listar Dueños existentes en base de datos completado con exito")
                print(f"{id_dueno}: {nombre_dueno}")

            try:
                dueno_id = input("\nIngrese el ID del dueño para ver sus mascotas: ")
                if not dueno_id.strip():
                    raise ValueError("Error! Este campo no puede estar vacio")
                else:
                    int(dueno_id)
            except ValueError as EmptyFieldError:
                logger.info("Proceso de listar Dueños por ID no se pudo completar debido a un error en los parametros requeridos")
                print(f"\n{EmptyFieldError}")
                continue

            mascotas = obtener_mascotas_por_dueno_sqlite(dueno_id)
            if not mascotas:
                logger.info(f"Proceso de Obtener Mascotas asociadas a ID Dueño no se pudo completar, no hay registros asociados a {dueno_id}")
                print("\nEste dueño no tiene mascotas registradas.")
                continue

            print("\nMascotas del dueño:")
            for id_mascota, nombre_mascota in mascotas:
                logger.info("Proceso de Listar Mascotas asociadas a Dueños existentes en base de datos completado con exito")
                print(f"{id_mascota}: {nombre_mascota}")

            try:
                mascota_id = input("\nID de la mascota: ")
                if not mascota_id.strip():
                    raise ValueError("Error! Este campo no puede estar vacio")
            except ValueError as EmptyFieldError:
                logger.info(f"Proceso de listar Mascotas asociadas a ID Dueño no se pudo completar no hay registros asociados a {mascota_id}")
                print(f"\n{EmptyFieldError}")
                continue

            historial = ver_historial_consultas_sqlite(mascota_id)
            if not historial:
                logger.info("Proceso de Ver Historia Consultas asociadas a mascotas existentes en base de datos no se pudo completar, no existen registros asociados")
                print("\nNo se encontró historial para esa mascota.")
            else:
                print("\nHistorial de consultas:")
                for fecha, motivo, diagnostico in historial:
                    logger.info("Proceso de Mostrar Historial de Consultas de Mascotas asociadas a Dueños existentes en base de datos completado con exito")
                    print(f"{fecha} - {motivo}: {diagnostico}")

        elif opcion == "7":
            logger.info("El usuario selecciono la opcion 'Actualizar datos de un dueño'")
            print("\n--- Actualizar Datos de Dueño ---")
            try:
                duenos = obtener_duenos_sqlite()
                if not duenos:
                    logger.info("Proceso de obtencion de Dueño en base de datos no se pudo completar, no existen registros asociados")
                    print("\nNo hay dueños registrados.")
                    print("\nDueños registrados:")
                for id_dueno, nombre_dueno in duenos:
                    logger.info("Proceso de Listar Dueños existentes en base de datos completado con exito")
                    print(f"{id_dueno}: {nombre_dueno}")

                dueno_id_str = input("Ingrese el ID del dueño a actualizar: ").strip()
                if not dueno_id_str.isdigit():
                    raise ValueError("Error! El ID debe ser un numero.")
                dueno_id = int(dueno_id_str)

                #Intentamos obtener el dueño para verificar si exise
                dueno_existente = obtener_duenos_sqlite()
                dueno_encontrado = False
                for d_id, d_nombre in dueno_existente:
                    if d_id == dueno_id:
                        print(f"Dueño actual : ID {d_id}, Nombre: {d_nombre}")
                        dueno_encontrado = True
                        break
                if not dueno_encontrado:
                    print(f"No se encontro un dueño con ID {dueno_id}.")
                    logger.warning(f"Intento de actualizar dueño con ID inexistente: {dueno_id}")
                    continue #Esto nos lleva al menu principal
                print("\nPor favor solo rellene los campos que desea actualizar:")
                nuevo_nombre = input("Nuevo nombre (actual...): ").strip()
                nuevo_telefono = input("Nuevo telefono (actual...): ").strip()
                nueva_direccion = input("Nuevo direccion (actual...): ").strip()

                # Convertimos cadenas vacías a None para la función de persistencia
                if not nuevo_nombre:
                    nuevo_nombre = None
                if not nuevo_telefono:
                    nuevo_telefono = None
                if not nueva_direccion:
                    nueva_direccion = None

                #Verificamos si al menos un campo tiene un nuevo valor
                if nuevo_nombre is None and nuevo_telefono is None and nueva_direccion is None:
                    print("No se ingresaron nuevos datos para actualizar")
                    logger.info(f"Actualizacion de dueño {dueno_id} no pudo ser completada por falta de datos")
                else:
                    #Llamamos a la funcion de persistencia
                    if actualizar_dueno_sqlite(dueno_id, nuevo_nombre, nuevo_telefono, nueva_direccion):
                        logger.info(f"Datos del dueño {dueno_id} actualizados con exito")
                        print(f"Datos del dueño {dueno_id} actualizados con exito")
                    else:
                        logger.warning(f"No se pudo actualizar el dueño con ID {dueno_id}.")
                        print(f"No se pudo actualizar el dueño con ID {dueno_id}. Verifique el ID.")

            except ValueError as ve:
                logger.error(f"Error de validación al actualizar dueño: {ve}")
                print(f"\nError: {ve}")
            except Exception as e:
                logger.critical(f"Error inesperado al actualizar dueño: {e}")
                print(f"\nOcurrió un error inesperado: {e}")

        elif opcion == "8":
            logger.info("Proceso de cierre de app completado con exito")
            print("\n¡Hasta luego!")
            break

        else:
            logger.info("Proceso de seleccion de opcion en el menu no se pudo completar debido a un error en los parametros requeridos")
            print("\nOpción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
