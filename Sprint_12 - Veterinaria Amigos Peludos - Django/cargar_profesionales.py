import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "veterinaria_web.settings")
django.setup()

from principal.models import Profesional

profesionales_data = [
    {"nombre_prof": "Dra. Camila Rodríguez", "tarjeta_profesional": "TPV001", "telefono": "3101234567", "especialidad": "Medicina Interna"},
    {"nombre_prof": "Dr. Andrés Gómez", "tarjeta_profesional": "TPV002", "telefono": "3159876543", "especialidad": "Cirugía General"},
    {"nombre_prof": "Dra. Laura Martínez", "tarjeta_profesional": "TPV003", "telefono": "3205552233", "especialidad": "Dermatología"},
    {"nombre_prof": "Dr. Carlos Pérez", "tarjeta_profesional": "TPV004", "telefono": "3113344556", "especialidad": "Urgencias"},
    {"nombre_prof": "Dra. Ana Morales", "tarjeta_profesional": "TPV005", "telefono": "3019988776", "especialidad": "Oftalmología"},
    {"nombre_prof": "Dr. Daniel Ruiz", "tarjeta_profesional": "TPV006", "telefono": "3124433221", "especialidad": "Ortopedia"},
    {"nombre_prof": "Dra. Natalia Vargas", "tarjeta_profesional": "TPV007", "telefono": "3165556677", "especialidad": "Neurología"},
    {"nombre_prof": "Dr. Juan David Torres", "tarjeta_profesional": "TPV008", "telefono": "3001122334", "especialidad": "Anestesiología"},
    {"nombre_prof": "Dra. Carolina Ríos", "tarjeta_profesional": "TPV009", "telefono": "3178787878", "especialidad": "Medicina Felina"},
    {"nombre_prof": "Dr. Sebastián León", "tarjeta_profesional": "TPV010", "telefono": "3189998888", "especialidad": "Medicina Canina"},
    {"nombre_prof": "Dra. Paola Mendoza", "tarjeta_profesional": "TPV011", "telefono": "3191234567", "especialidad": "Rehabilitación"},
    {"nombre_prof": "Dr. Alejandro Castaño", "tarjeta_profesional": "TPV012", "telefono": "3117775554", "especialidad": "Patología"},
    {"nombre_prof": "Dra. Isabel Herrera", "tarjeta_profesional": "TPV013", "telefono": "3107773332", "especialidad": "Odontología Veterinaria"},
    {"nombre_prof": "Dr. Felipe Ramírez", "tarjeta_profesional": "TPV014", "telefono": "3028889990", "especialidad": "Medicina Preventiva"},
    {"nombre_prof": "Dra. Mariana Salazar", "tarjeta_profesional": "TPV015", "telefono": "3214446677", "especialidad": "Etología"},
    {"nombre_prof": "Dr. Jorge Acosta", "tarjeta_profesional": "TPV016", "telefono": "3136667788", "especialidad": "Exóticos"},
    {"nombre_prof": "Dra. Mónica Delgado", "tarjeta_profesional": "TPV017", "telefono": "3201112223", "especialidad": "Cardiología"},
    {"nombre_prof": "Dr. David Beltrán", "tarjeta_profesional": "TPV018", "telefono": "3147896541", "especialidad": "Oncología"},
    {"nombre_prof": "Dra. Juliana Ibáñez", "tarjeta_profesional": "TPV019", "telefono": "3194567890", "especialidad": "Gastroenterología"},
    {"nombre_prof": "Dr. Santiago Nieto", "tarjeta_profesional": "TPV020", "telefono": "3004445566", "especialidad": "Ecografía Veterinaria"},
]

for prof in profesionales_data:
    obj, creado = Profesional.objects.get_or_create(
        tarjeta_profesional=prof["tarjeta_profesional"],
        defaults=prof
    )
    if creado:
        print(f"✓ Agregado: {obj.nombre_prof}")
    else:
        print(f"- Ya existía: {obj.nombre_prof}")
