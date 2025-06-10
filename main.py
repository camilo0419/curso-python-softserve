from conexion import crear_tablas
from logger import logger
from persistencia import (
    registrar_dueno_sqlite,
    obtener_duenos_sqlite,
    registrar_mascota_sqlite,
    obtener_mascotas_por_dueno_sqlite,
    registrar_consulta_sqlite,
    ver_historial_consultas_sqlite,
    actualizar_dueno_sqlite,
    actualizar_mascota_sqlite,
    actualizar_consulta_sqlite,
    eliminar_dueno_logicamente_sqlite,
    eliminar_consulta_logicamente_sqlite,
    eliminar_mascota_logicamente_sqlite,
    obtener_consultas_con_id_sqlite
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
        print("7. Actualizar datos")
        print("8. Eliminar registros")
        print("9. Salir")

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
            logger.info("El usuario selecciono la opcion 'Actualizar datos'")
            while True:
                print("\n--- Sub-menú de Actualización ---")
                print("1. Actualizar datos de un dueño")
                print("2. Actualizar datos de una mascota") 
                print("3. Actualizar datos de una consulta")
                print("4. Volver al menú principal")

                sub_opcion_actualizar = input("\nSeleccione una opción de actualización: ")

                if sub_opcion_actualizar == "1":
                    try:
                        duenos = obtener_duenos_sqlite() 
                        if not duenos:
                            logger.info("Proceso de obtencion de Dueño en base de datos no se pudo completar, no existen registros asociados")
                            print("\nNo hay dueños registrados para actualizar.")
                            continue
                        
                        print("\nDueños registrados:")
                        for id_dueno, nombre_dueno in duenos:
                            logger.info(f"Dueño listado: ID {id_dueno}, Nombre: {nombre_dueno}") 
                            print(f"ID {id_dueno}: {nombre_dueno}")
                                            
                        dueno_id_str = input("\nIngrese el ID del dueño a actualizar: ").strip()
                        if not dueno_id_str.isdigit():
                            raise ValueError("Error! El ID debe ser un número.")
                        dueno_id = int(dueno_id_str)

                        dueno_existe = False
                        for d_id, _ in duenos: 
                            if d_id == dueno_id:
                                dueno_existe = True
                                break
                        
                        if not dueno_existe:
                            print(f"No se encontró un dueño con ID {dueno_id}.")
                            logger.warning(f"Intento de actualizar dueño con ID inexistente: {dueno_id}")
                            continue

                        print("\nDeje en blanco los campos que no desee actualizar.")
                        nuevo_nombre = input("Nuevo nombre: ").strip()
                        nuevo_telefono = input("Nuevo teléfono: ").strip()
                        nueva_direccion = input("Nueva dirección: ").strip()

                        if not nuevo_nombre:
                            nuevo_nombre = None
                        if not nuevo_telefono:
                            nuevo_telefono = None
                        if not nueva_direccion:
                            nueva_direccion = None

                        if nuevo_nombre is None and nuevo_telefono is None and nueva_direccion is None:
                            print("No se ingresaron nuevos datos para actualizar.")
                            logger.info(f"Actualización de dueño {dueno_id} cancelada por falta de datos.")
                        else:
                            if actualizar_dueno_sqlite(dueno_id, nuevo_nombre, nuevo_telefono, nueva_direccion):
                                logger.info(f"Datos del dueño con ID {dueno_id} actualizados con éxito.")
                                print(f"Datos del dueño con ID {dueno_id} actualizados con éxito.")
                            else:
                                logger.warning(f"No se pudo actualizar el dueño con ID {dueno_id}.")
                                print(f"No se pudo actualizar el dueño con ID {dueno_id}. Verifique el ID.")

                    except ValueError as ve:
                        logger.error(f"Error de validación al actualizar dueño: {ve}")
                        print(f"\nError: {ve}")
                    except Exception as e:
                        logger.critical(f"Error inesperado al actualizar dueño: {e}")
                        print(f"\nOcurrió un error inesperado: {e}")

                elif sub_opcion_actualizar == "2":
                    # Lógica para actualizar mascota
                    print("\n--- Actualizar Datos de una Mascota ---")
                    try:
                        # Primero, listar dueños para que el usuario elija
                        duenos_activos = obtener_duenos_sqlite()
                        if not duenos_activos:
                            print("\nNo hay dueños activos para buscar mascotas.")
                            logger.warning("Intento de actualizar mascota sin dueños activos.")
                            continue

                        print("\nDueños activos:")
                        for d_id, d_nombre in duenos_activos:
                            print(f"ID {d_id}: {d_nombre}")

                        dueno_id_mascota_str = input("Ingrese el ID del dueño de la mascota a actualizar: ").strip()
                        if not dueno_id_mascota_str.isdigit():
                            raise ValueError("Error! El ID del dueño debe ser un número.")
                        dueno_id_mascota = int(dueno_id_mascota_str)

                        if not any(d_id == dueno_id_mascota for d_id, _ in duenos_activos):
                            print(f"No se encontró un dueño activo con ID {dueno_id_mascota}.")
                            logger.warning(f"Intento de actualizar mascota para dueño inexistente o inactivo: {dueno_id_mascota}")
                            continue

                        # Luego, listar mascotas activas de ese dueño
                        mascotas_dueno = obtener_mascotas_por_dueno_sqlite(dueno_id_mascota)
                        if not mascotas_dueno:
                            print(f"\nNo hay mascotas activas para el dueño ID {dueno_id_mascota}.")
                            logger.info(f"No hay mascotas activas para dueño {dueno_id_mascota} para actualizar.")
                            continue

                        print(f"\nMascotas activas del dueño ID {dueno_id_mascota}:")
                        for m_id, m_nombre in mascotas_dueno:
                            print(f"ID {m_id}: {m_nombre}")

                        mascota_id_actualizar_str = input("Ingrese el ID de la mascota a actualizar: ").strip()
                        if not mascota_id_actualizar_str.isdigit():
                            raise ValueError("Error! El ID de la mascota debe ser un número.")
                        mascota_id_actualizar = int(mascota_id_actualizar_str)

                        mascota_encontrada_activa = False
                        for m_id, _ in mascotas_dueno:
                            if m_id == mascota_id_actualizar:
                                mascota_encontrada_activa = True
                                break
                        
                        if not mascota_encontrada_activa:
                            print(f"No se encontró una mascota activa con ID {mascota_id_actualizar} para el dueño {dueno_id_mascota}.")
                            logger.warning(f"Intento de actualizar mascota inexistente o inactiva: {mascota_id_actualizar} (dueño {dueno_id_mascota})")
                            continue

                        print("\nDeje en blanco los campos que no desee actualizar.")
                        nuevo_nombre = input("Nuevo nombre de la mascota: ").strip()
                        nueva_especie = input("Nueva especie: ").strip()
                        nueva_raza = input("Nueva raza: ").strip()
                        nueva_edad_str = input("Nueva edad: ").strip()

                        if not nuevo_nombre:
                            nuevo_nombre = None
                        if not nueva_especie:
                            nueva_especie = None
                        if not nueva_raza:
                            nueva_raza = None
                        
                        nueva_edad = None
                        if nueva_edad_str:
                            if not nueva_edad_str.isdigit():
                                raise ValueError("Error! La edad debe ser un número.")
                            nueva_edad = int(nueva_edad_str)

                        if nuevo_nombre is None and nueva_especie is None and nueva_raza is None and nueva_edad is None:
                            print("No se ingresaron nuevos datos para actualizar.")
                            logger.info(f"Actualización de mascota {mascota_id_actualizar} cancelada por falta de datos.")
                        else:
                            if actualizar_mascota_sqlite(mascota_id_actualizar, nuevo_nombre, nueva_especie, nueva_raza, nueva_edad):
                                logger.info(f"Datos de la mascota con ID {mascota_id_actualizar} actualizados con éxito.")
                                print(f"Datos de la mascota con ID {mascota_id_actualizar} actualizados con éxito.")
                            else:
                                logger.warning(f"No se pudo actualizar la mascota con ID {mascota_id_actualizar}.")
                                print(f"No se pudo actualizar la mascota con ID {mascota_id_actualizar}. Verifique el ID.")

                    except ValueError as ve:
                        logger.error(f"Error de validación al actualizar mascota: {ve}")
                        print(f"\nError: {ve}")
                    except Exception as e:
                        logger.critical(f"Error inesperado al actualizar mascota: {e}")
                        print(f"\nOcurrió un error inesperado: {e}")

                elif sub_opcion_actualizar == "3":
                    # Lógica para actualizar consulta
                    print("\n--- Actualizar Datos de una Consulta ---")
                    try:
                        # Primero, listar dueños para buscar la mascota
                        duenos_activos = obtener_duenos_sqlite()
                        if not duenos_activos:
                            print("\nNo hay dueños activos para buscar consultas.")
                            logger.warning("Intento de actualizar consulta sin dueños activos.")
                            continue

                        print("\nDueños activos:")
                        for d_id, d_nombre in duenos_activos:
                            print(f"ID {d_id}: {d_nombre}")

                        dueno_id_consulta_str = input("Ingrese el ID del dueño de la mascota cuya consulta desea actualizar: ").strip()
                        if not dueno_id_consulta_str.isdigit():
                            raise ValueError("Error! El ID del dueño debe ser un número.")
                        dueno_id_consulta = int(dueno_id_consulta_str)

                        if not any(d_id == dueno_id_consulta for d_id, _ in duenos_activos):
                            print(f"No se encontró un dueño activo con ID {dueno_id_consulta}.")
                            logger.warning(f"Intento de actualizar consulta para dueño inexistente o inactivo: {dueno_id_consulta}")
                            continue

                        # Luego, listar mascotas activas de ese dueño
                        mascotas_dueno = obtener_mascotas_por_dueno_sqlite(dueno_id_consulta)
                        if not mascotas_dueno:
                            print(f"\nNo hay mascotas activas para el dueño ID {dueno_id_consulta}.")
                            logger.info(f"No hay mascotas activas para dueño {dueno_id_consulta} para actualizar sus consultas.")
                            continue

                        print(f"\nMascotas activas del dueño ID {dueno_id_consulta}:")
                        for m_id, m_nombre in mascotas_dueno:
                            print(f"ID {m_id}: {m_nombre}")

                        mascota_id_consulta_str = input("Ingrese el ID de la mascota cuya consulta desea actualizar: ").strip()
                        if not mascota_id_consulta_str.isdigit():
                            raise ValueError("Error! El ID de la mascota debe ser un número.")
                        mascota_id_consulta = int(mascota_id_consulta_str)

                        mascota_encontrada_para_consulta = False
                        for m_id, _ in mascotas_dueno:
                            if m_id == mascota_id_consulta:
                                mascota_encontrada_para_consulta = True
                                break
                        
                        if not mascota_encontrada_para_consulta:
                            print(f"No se encontró una mascota activa con ID {mascota_id_consulta} para el dueño {dueno_id_consulta}.")
                            logger.warning(f"Intento de actualizar consulta para mascota inexistente o inactiva: {mascota_id_consulta} (dueño {dueno_id_consulta})")
                            continue
                        
                        # Ahora, listar las consultas de esa mascota incluyendo su ID
                        consultas_mascota = obtener_consultas_con_id_sqlite(mascota_id_consulta)
                        if not consultas_mascota:
                            print(f"\nNo hay consultas activas para la mascota ID {mascota_id_consulta}.")
                            logger.info(f"No hay consultas activas para la mascota {mascota_id_consulta} para actualizar.")
                            continue

                        print(f"\nConsultas activas de la mascota ID {mascota_id_consulta}:")
                        for c_id, fecha, motivo, diagnostico in consultas_mascota:
                            print(f"ID: {c_id}, Fecha: {fecha}, Motivo: {motivo}, Diagnóstico: {diagnostico}")
                        
                        consulta_id_actualizar_str = input("Ingrese el ID de la consulta a actualizar: ").strip()
                        if not consulta_id_actualizar_str.isdigit():
                            raise ValueError("Error! El ID de la consulta debe ser un número.")
                        consulta_id_actualizar = int(consulta_id_actualizar_str)

                        consulta_encontrada_activa = False
                        for c_id, _, _, _ in consultas_mascota:
                            if c_id == consulta_id_actualizar:
                                consulta_encontrada_activa = True
                                break
                        
                        if not consulta_encontrada_activa:
                            print(f"No se encontró una consulta activa con ID {consulta_id_actualizar} para la mascota {mascota_id_consulta}.")
                            logger.warning(f"Intento de actualizar consulta inexistente o ya inactiva: {consulta_id_actualizar} (mascota {mascota_id_consulta})")
                            continue

                        print("\nDeje en blanco los campos que no desee actualizar.")
                        nueva_fecha = input("Nueva fecha (YYYY-MM-DD): ").strip()
                        nuevo_motivo = input("Nuevo motivo: ").strip()
                        nuevo_diagnostico = input("Nuevo diagnóstico: ").strip()

                        if not nueva_fecha:
                            nueva_fecha = None
                        if not nuevo_motivo:
                            nuevo_motivo = None
                        if not nuevo_diagnostico:
                            nuevo_diagnostico = None

                        if nueva_fecha is None and nuevo_motivo is None and nuevo_diagnostico is None:
                            print("No se ingresaron nuevos datos para actualizar.")
                            logger.info(f"Actualización de consulta {consulta_id_actualizar} cancelada por falta de datos.")
                        else:
                            if actualizar_consulta_sqlite(consulta_id_actualizar, nueva_fecha, nuevo_motivo, nuevo_diagnostico):
                                logger.info(f"Datos de la consulta con ID {consulta_id_actualizar} actualizados con éxito.")
                                print(f"Datos de la consulta con ID {consulta_id_actualizar} actualizados con éxito.")
                            else:
                                logger.warning(f"No se pudo actualizar la consulta con ID {consulta_id_actualizar}.")
                                print(f"No se pudo actualizar la consulta con ID {consulta_id_actualizar}. Verifique el ID.")

                    except ValueError as ve:
                        logger.error(f"Error de validación al actualizar consulta: {ve}")
                        print(f"\nError: {ve}")
                    except Exception as e:
                        logger.critical(f"Error inesperado al actualizar consulta: {e}")
                        print(f"\nOcurrió un error inesperado: {e}")
                elif sub_opcion_actualizar == "4":
                    logger.info("El usuario regresó del sub-menú de actualización.")
                    break # Sale del sub-menú y vuelve al menú principal
                else:
                    print("Opción no válida. Intente nuevamente.")

        elif opcion == "8":
            logger.info("El usuario selecciono la opcion 'Eliminar registros (lógicamente)'")
            while True:
                print("\n--- Sub-menú de Eliminación ---")
                print("1. Eliminar dueño")
                print("2. Eliminar mascota")
                print("3. Eliminar consulta")
                print("4. Volver al menú principal")

                sub_opcion_eliminar = input("\nSeleccione una opción de eliminación: ")

                if sub_opcion_eliminar == "1":
                    try:
                        duenos = obtener_duenos_sqlite() 
                        if not duenos:
                            logger.info("No hay dueños activos registrados para eliminar.")
                            print("\nNo hay dueños activos registrados para eliminar.")
                            continue
                        
                        print("\nDueños activos registrados (ID: Nombre):")
                        for id_dueno, nombre_dueno in duenos:
                            print(f"ID {id_dueno}: {nombre_dueno}")
                                            
                        dueno_id_str = input("\nIngrese el ID del dueño a eliminar lógicamente: ").strip()
                        if not dueno_id_str.isdigit():
                            raise ValueError("Error! El ID debe ser un número.")
                        dueno_id = int(dueno_id_str)

                        dueno_existe_activo = False
                        for d_id, _ in duenos: 
                            if d_id == dueno_id:
                                dueno_existe_activo = True
                                break
                        
                        if not dueno_existe_activo:
                            print(f"No se encontró un dueño activo con ID {dueno_id}.")
                            logger.warning(f"Intento de eliminar lógicamente dueño inexistente o ya inactivo: {dueno_id}")
                            continue

                        confirmacion = input(f"¿Está seguro de que desea eliminar lógicamente al dueño con ID {dueno_id}? (s/n): ").strip().lower()
                        if confirmacion == 's':
                            if eliminar_dueno_logicamente_sqlite(dueno_id):
                                logger.info(f"Dueño con ID {dueno_id} eliminado lógicamente con éxito.")
                                print(f"Dueño con ID {dueno_id} eliminado lógicamente con éxito.")
                            else:
                                logger.warning(f"No se pudo eliminar lógicamente al dueño con ID {dueno_id}.")
                                print(f"No se pudo eliminar lógicamente al dueño con ID {dueno_id}.")
                        else:
                            print("Eliminación cancelada.")
                            logger.info(f"Eliminación lógica de dueño {dueno_id} cancelada por el usuario.")

                    except ValueError as ve:
                        logger.error(f"Error de validación al eliminar dueño lógicamente: {ve}")
                        print(f"\nError: {ve}")
                    except Exception as e:
                        logger.critical(f"Error inesperado al eliminar dueño lógicamente: {e}")
                        print(f"\nOcurrió un error inesperado: {e}")

                elif sub_opcion_eliminar == "2":
                    # Lógica para eliminar mascota lógicamente
                    print("\n--- Eliminar Mascota ---")
                    try:
                        # Para listar las mascotas disponibles para eliminar,
                        # necesitaríamos una función en persistencia.py que obtenga *todas* las mascotas activas.
                        # Por ahora, puedes pedir el ID directamente o crear esa función.
                        # Para mantener la misma lógica, vamos a obtenerlas por dueño.
                        duenos_activos = obtener_duenos_sqlite()
                        if not duenos_activos:
                            print("\nNo hay dueños activos para buscar mascotas.")
                            logger.warning("Intento de eliminar mascota sin dueños activos.")
                            continue

                        print("\nDueños activos (para buscar mascotas):")
                        for d_id, d_nombre in duenos_activos:
                            print(f"ID {d_id}: {d_nombre}")

                        dueno_id_mascota_str = input("Ingrese el ID del dueño de la mascota a eliminar: ").strip()
                        if not dueno_id_mascota_str.isdigit():
                            raise ValueError("Error! El ID del dueño debe ser un número.")
                        dueno_id_mascota = int(dueno_id_mascota_str)

                        # Verificamos si el dueño existe y es activo
                        if not any(d_id == dueno_id_mascota for d_id, _ in duenos_activos):
                            print(f"No se encontró un dueño activo con ID {dueno_id_mascota}.")
                            logger.warning(f"Intento de eliminar mascota para dueño inexistente o inactivo: {dueno_id_mascota}")
                            continue

                        mascotas_dueno = obtener_mascotas_por_dueno_sqlite(dueno_id_mascota)
                        if not mascotas_dueno:
                            print(f"\nNo hay mascotas activas para el dueño ID {dueno_id_mascota}.")
                            logger.info(f"No hay mascotas activas para dueño {dueno_id_mascota} para eliminar.")
                            continue

                        print(f"\nMascotas activas del dueño ID {dueno_id_mascota}:")
                        for m_id, m_nombre in mascotas_dueno:
                            print(f"ID {m_id}: {m_nombre}")

                        mascota_id_eliminar_str = input("Ingrese el ID de la mascota a eliminar: ").strip()
                        if not mascota_id_eliminar_str.isdigit():
                            raise ValueError("Error! El ID de la mascota debe ser un número.")
                        mascota_id_eliminar = int(mascota_id_eliminar_str)

                        # Verificamos si la mascota existe y es activa para este dueño
                        mascota_encontrada_activa = False
                        for m_id, _ in mascotas_dueno:
                            if m_id == mascota_id_eliminar:
                                mascota_encontrada_activa = True
                                break
                        
                        if not mascota_encontrada_activa:
                            print(f"No se encontró una mascota activa con ID {mascota_id_eliminar} para el dueño {dueno_id_mascota}.")
                            logger.warning(f"Intento de eliminar mascota inexistente o ya inactiva: {mascota_id_eliminar} (dueño {dueno_id_mascota})")
                            continue

                        confirmacion = input(f"¿Está seguro de que desea eliminar a la mascota con ID {mascota_id_eliminar}? (s/n): ").strip().lower()
                        if confirmacion == 's':
                            if eliminar_mascota_logicamente_sqlite(mascota_id_eliminar):
                                logger.info(f"Mascota con ID {mascota_id_eliminar} eliminada lógicamente con éxito.")
                                print(f"Mascota con ID {mascota_id_eliminar} eliminada con éxito.")
                            else:
                                logger.warning(f"No se pudo eliminar lógicamente a la mascota con ID {mascota_id_eliminar}.")
                                print(f"No se pudo eliminar a la mascota con ID {mascota_id_eliminar}.")
                        else:
                            print("Eliminación cancelada.")
                            logger.info(f"Eliminación lógica de mascota {mascota_id_eliminar} cancelada por el usuario.")

                    except ValueError as ve:
                        logger.error(f"Error de validación al eliminar mascota lógicamente: {ve}")
                        print(f"\nError: {ve}")
                    except Exception as e:
                        logger.critical(f"Error inesperado al eliminar mascota lógicamente: {e}")
                        print(f"\nOcurrió un error inesperado: {e}")


                elif sub_opcion_eliminar == "3":
                    # Lógica para eliminar consulta lógicamente
                    print("\n--- Eliminar Consulta ---")
                    try:
                        # Para listar las consultas disponibles para eliminar,
                        # necesitaríamos una función en persistencia.py que obtenga *todas* las consultas activas,
                        # o al menos por mascota.
                        # Para mantener la misma lógica, vamos a pedir el ID de la mascota y luego listar sus consultas.
                        
                        # Primero listar dueños activos para buscar mascota
                        duenos_activos = obtener_duenos_sqlite()
                        if not duenos_activos:
                            print("\nNo hay dueños activos para buscar mascotas y sus consultas.")
                            logger.warning("Intento de eliminar consulta sin dueños activos.")
                            continue

                        print("\nDueños activos (para buscar mascotas y sus consultas):")
                        for d_id, d_nombre in duenos_activos:
                            print(f"ID {d_id}: {d_nombre}")

                        dueno_id_consulta_str = input("Ingrese el ID del dueño de la mascota cuya consulta desea eliminar: ").strip()
                        if not dueno_id_consulta_str.isdigit():
                            raise ValueError("Error! El ID del dueño debe ser un número.")
                        dueno_id_consulta = int(dueno_id_consulta_str)

                        if not any(d_id == dueno_id_consulta for d_id, _ in duenos_activos):
                            print(f"No se encontró un dueño activo con ID {dueno_id_consulta}.")
                            logger.warning(f"Intento de eliminar consulta para dueño inexistente o inactivo: {dueno_id_consulta}")
                            continue

                        mascotas_dueno_consulta = obtener_mascotas_por_dueno_sqlite(dueno_id_consulta)
                        if not mascotas_dueno_consulta:
                            print(f"\nNo hay mascotas activas para el dueño ID {dueno_id_consulta}.")
                            logger.info(f"No hay mascotas activas para dueño {dueno_id_consulta} para eliminar sus consultas.")
                            continue

                        print(f"\nMascotas activas del dueño ID {dueno_id_consulta}:")
                        for m_id, m_nombre in mascotas_dueno_consulta:
                            print(f"ID {m_id}: {m_nombre}")

                        mascota_id_consulta_str = input("Ingrese el ID de la mascota cuya consulta desea eliminar: ").strip()
                        if not mascota_id_consulta_str.isdigit():
                            raise ValueError("Error! El ID de la mascota debe ser un número.")
                        mascota_id_consulta = int(mascota_id_consulta_str)

                        mascota_encontrada_para_consulta = False
                        for m_id, _ in mascotas_dueno_consulta:
                            if m_id == mascota_id_consulta:
                                mascota_encontrada_para_consulta = True
                                break
                        
                        if not mascota_encontrada_para_consulta:
                            print(f"No se encontró una mascota activa con ID {mascota_id_consulta} para el dueño {dueno_id_consulta}.")
                            logger.warning(f"Intento de eliminar consulta para mascota inexistente o inactiva: {mascota_id_consulta} (dueño {dueno_id_consulta})")
                            continue
                        
                        consultas_mascota = obtener_consultas_con_id_sqlite(mascota_id_consulta)

                        if not consultas_mascota:
                            print(f"\nNo hay consultas activas para la mascota ID {mascota_id_consulta}.")
                            logger.info(f"No hay consultas activas para la mascota {mascota_id_consulta} para eliminar.")
                            continue
                        
                        print(f"\nConsultas activas de la mascota ID {mascota_id_consulta}:")
                        for c_id, fecha, motivo, diagnostico in consultas_mascota:
                            # Una forma más sencilla de mostrar la información por línea
                            print(f"ID: {c_id}, Fecha: {fecha}, Motivo: {motivo}, Diagnóstico: {diagnostico}")

                        consulta_id_eliminar_str = input("Ingrese el ID de la consulta a eliminar lógicamente: ").strip()
                        if not consulta_id_eliminar_str.isdigit():
                            raise ValueError("Error! El ID de la consulta debe ser un número.")
                        consulta_id_eliminar = int(consulta_id_eliminar_str)
                        
                        # --- Verificamos si la consulta existe y es activa para la mascota ---
                        consulta_encontrada_activa = False
                        for c_id, _, _, _ in consultas_mascota:
                            if c_id == consulta_id_eliminar:
                                consulta_encontrada_activa = True
                                break
                        
                        if not consulta_encontrada_activa:
                            print(f"No se encontró una consulta activa con ID {consulta_id_eliminar} para la mascota {mascota_id_consulta}.")
                            logger.warning(f"Intento de eliminar consulta inexistente o ya inactiva: {consulta_id_eliminar} (mascota {mascota_id_consulta})")
                            continue

                        confirmacion = input(f"¿Está seguro de que desea eliminar la consulta con ID {consulta_id_eliminar}? (s/n): ").strip().lower()
                        if confirmacion == 's':
                            if eliminar_consulta_logicamente_sqlite(consulta_id_eliminar):
                                logger.info(f"Consulta con ID {consulta_id_eliminar} eliminada lógicamente con éxito.")
                                print(f"Consulta con ID {consulta_id_eliminar} eliminada con éxito.")
                            else:
                                logger.warning(f"No se pudo eliminar lógicamente la consulta con ID {consulta_id_eliminar}.")
                                print(f"No se pudo eliminar la consulta con ID {consulta_id_eliminar}.")
                        else:
                            print("Eliminación cancelada.")
                            logger.info(f"Eliminación lógica de consulta {consulta_id_eliminar} cancelada por el usuario.")

                    except ValueError as ve:
                        logger.error(f"Error de validación al eliminar consulta lógicamente: {ve}")
                        print(f"\nError: {ve}")
                    except Exception as e:
                        logger.critical(f"Error inesperado al eliminar consulta lógicamente: {e}")
                        print(f"\nOcurrió un error inesperado: {e}")


                elif sub_opcion_eliminar == "4":
                    logger.info("El usuario regresó del sub-menú de eliminación lógica.")
                    break # Sale del sub-menú y vuelve al menú principal
                else:
                    print("Opción no válida. Intente nuevamente.")

        elif opcion == "9":
            logger.info("Proceso de cierre de app completado con exito")
            print("\n¡Hasta luego!")
            break

        else:
            logger.info("Proceso de seleccion de opcion en el menu no se pudo completar debido a un error en los parametros requeridos")
            print("\nOpción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
