🐾 Veterinaria Amigos Peludos

Sistema de gestión para una clínica veterinaria, desarrollado con Django. Permite administrar clientes, mascotas, consultas, fórmulas médicas, medicamentos, profesionales y cirugías. 

📦 Módulos y funcionalidades

👤 Clientes
Crear, editar y eliminación lógica de clientes.

Buscar clientes por nombre o cédula.

Asociar mascotas por cliente.

Validación: Verificar listado y prueba de búsqueda.

🐾 Mascotas
Registro, edición y eliminación lógica.

Filtrado por cliente.

Validación: Asociar con cliente y verificar si se ocultan mascotas eliminadas.


📋 Consultas
Registro completo de consultas veterinarias.

Diagnóstico, requerimiento de medicamentos o cirugías.

Vista de detalle por cada consulta.

Validación: Crear consulta → Asignar medicamentos o cirugía → Visualizar historial.


🧾 Fórmulas Médicas
Generación de fórmulas con múltiples medicamentos.

Impresión solo si hay medicamentos y están entregados.

Marcado como entregado.

Validación: Crear fórmula, entregar y verificar restricción de impresión.


💊 Medicamentos
CRUD completo con eliminación lógica.

Paginación y buscador.

Exportación a Excel.

Validación: Crear, eliminar y confirmar que el stock no aparece si está inactivo.


🩺 Profesionales
Gestión de profesionales (alta, edición, baja).

Paginación y búsqueda por especialidad.

Validación: Crear profesional y asignar en cirugías.


🗓️ Cirugías
Programación desde consultas o directamente.

Solo permite marcar como realizada si está activa.

Cancelación lógica y visualización de estado (programada, realizada, cancelada).

Vista de cirugías pendientes o incompletas.

Validación: Crear cirugía desde consulta y desde módulo, cambiar estado.


📤 Exportaciones
Exportar todos los módulos (clientes, mascotas, medicamentos, etc.) a Excel.

Validación: Click en botón "Exportar a Excel" en cada módulo → archivo descargado.


📚 Seguridad y registro
Todas las acciones importantes quedan registradas usando el sistema de logging.

Los errores se almacenan en veterinaria.log.

Se aplica protección CSRF en formularios sensibles.

👨‍💻 Autores
Desarrollado por:
Camilo Vargas y Andrés Zuleta 2025.