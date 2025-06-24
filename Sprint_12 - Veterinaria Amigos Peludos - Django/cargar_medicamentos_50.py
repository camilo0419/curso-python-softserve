import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "veterinaria_web.settings")
django.setup()

from principal.models import Medicamento

medicamentos_data = [
    {'nombre_med': 'Doxiciclina 587', 'presentacion': 'Jarabe', 'stock_disponible': 31, 'fecha_vencimiento': '2026-04-05'},
    {'nombre_med': 'Doxiciclina 740', 'presentacion': 'Inyectable', 'stock_disponible': 25, 'fecha_vencimiento': '2026-05-04'},
    {'nombre_med': 'Furosemida 193', 'presentacion': 'Inyectable', 'stock_disponible': 92, 'fecha_vencimiento': '2026-08-26'},
    {'nombre_med': 'Prednisolona 146', 'presentacion': 'Crema', 'stock_disponible': 11, 'fecha_vencimiento': '2027-01-13'},
    {'nombre_med': 'Furosemida 247', 'presentacion': 'Crema', 'stock_disponible': 18, 'fecha_vencimiento': '2027-01-03'},
    {'nombre_med': 'Ketoprofeno 822', 'presentacion': 'Tableta', 'stock_disponible': 59, 'fecha_vencimiento': '2026-11-27'},
    {'nombre_med': 'Cefalexina 687', 'presentacion': 'Jarabe', 'stock_disponible': 14, 'fecha_vencimiento': '2026-09-27'},
    {'nombre_med': 'Amoxicilina 797', 'presentacion': 'Solución oral', 'stock_disponible': 58, 'fecha_vencimiento': '2026-11-10'},
    {'nombre_med': 'Prednisolona 411', 'presentacion': 'Tableta', 'stock_disponible': 37, 'fecha_vencimiento': '2026-03-08'},
    {'nombre_med': 'Clindamicina 520', 'presentacion': 'Crema', 'stock_disponible': 13, 'fecha_vencimiento': '2026-02-16'},
    {'nombre_med': 'Prednisolona 888', 'presentacion': 'Inyectable', 'stock_disponible': 25, 'fecha_vencimiento': '2026-01-28'},
    {'nombre_med': 'Clindamicina 574', 'presentacion': 'Tableta', 'stock_disponible': 12, 'fecha_vencimiento': '2027-05-03'},
    {'nombre_med': 'Furosemida 660', 'presentacion': 'Inyectable', 'stock_disponible': 77, 'fecha_vencimiento': '2026-08-08'},
    {'nombre_med': 'Ivermectina 877', 'presentacion': 'Tableta', 'stock_disponible': 10, 'fecha_vencimiento': '2026-09-01'},
    {'nombre_med': 'Clindamicina 597', 'presentacion': 'Inyectable', 'stock_disponible': 29, 'fecha_vencimiento': '2026-12-09'},
    {'nombre_med': 'Furosemida 671', 'presentacion': 'Inyectable', 'stock_disponible': 81, 'fecha_vencimiento': '2026-12-24'},
    {'nombre_med': 'Clindamicina 334', 'presentacion': 'Tableta', 'stock_disponible': 56, 'fecha_vencimiento': '2027-03-16'},
    {'nombre_med': 'Amoxicilina 983', 'presentacion': 'Tableta', 'stock_disponible': 62, 'fecha_vencimiento': '2026-07-03'},
    {'nombre_med': 'Ivermectina 825', 'presentacion': 'Solución oral', 'stock_disponible': 82, 'fecha_vencimiento': '2026-04-07'},
    {'nombre_med': 'Enrofloxacina 577', 'presentacion': 'Solución oral', 'stock_disponible': 63, 'fecha_vencimiento': '2026-05-23'},
    {'nombre_med': 'Ketoprofeno 720', 'presentacion': 'Tableta', 'stock_disponible': 38, 'fecha_vencimiento': '2026-05-15'},
    {'nombre_med': 'Amoxicilina 688', 'presentacion': 'Solución oral', 'stock_disponible': 12, 'fecha_vencimiento': '2026-06-10'},
    {'nombre_med': 'Amoxicilina 102', 'presentacion': 'Solución oral', 'stock_disponible': 78, 'fecha_vencimiento': '2027-06-12'},
    {'nombre_med': 'Furosemida 838', 'presentacion': 'Inyectable', 'stock_disponible': 12, 'fecha_vencimiento': '2027-04-06'},
    {'nombre_med': 'Doxiciclina 343', 'presentacion': 'Crema', 'stock_disponible': 11, 'fecha_vencimiento': '2026-07-20'},
    {'nombre_med': 'Furosemida 384', 'presentacion': 'Jarabe', 'stock_disponible': 67, 'fecha_vencimiento': '2026-03-24'},
    {'nombre_med': 'Furosemida 780', 'presentacion': 'Inyectable', 'stock_disponible': 17, 'fecha_vencimiento': '2026-05-15'},
    {'nombre_med': 'Cefalexina 410', 'presentacion': 'Solución oral', 'stock_disponible': 40, 'fecha_vencimiento': '2026-09-27'},
    {'nombre_med': 'Doxiciclina 262', 'presentacion': 'Solución oral', 'stock_disponible': 48, 'fecha_vencimiento': '2027-04-08'},
    {'nombre_med': 'Ivermectina 618', 'presentacion': 'Solución oral', 'stock_disponible': 86, 'fecha_vencimiento': '2027-03-22'},
    {'nombre_med': 'Ivermectina 687', 'presentacion': 'Crema', 'stock_disponible': 43, 'fecha_vencimiento': '2026-04-24'},
    {'nombre_med': 'Doxiciclina 236', 'presentacion': 'Crema', 'stock_disponible': 49, 'fecha_vencimiento': '2026-11-20'},
    {'nombre_med': 'Metronidazol 376', 'presentacion': 'Inyectable', 'stock_disponible': 86, 'fecha_vencimiento': '2026-08-11'},
    {'nombre_med': 'Metronidazol 560', 'presentacion': 'Inyectable', 'stock_disponible': 92, 'fecha_vencimiento': '2026-08-11'},
    {'nombre_med': 'Clindamicina 417', 'presentacion': 'Solución oral', 'stock_disponible': 15, 'fecha_vencimiento': '2026-01-24'},
    {'nombre_med': 'Clindamicina 667', 'presentacion': 'Tableta', 'stock_disponible': 71, 'fecha_vencimiento': '2027-03-16'},
    {'nombre_med': 'Enrofloxacina 576', 'presentacion': 'Inyectable', 'stock_disponible': 75, 'fecha_vencimiento': '2026-10-26'},
    {'nombre_med': 'Ketoprofeno 521', 'presentacion': 'Solución oral', 'stock_disponible': 16, 'fecha_vencimiento': '2026-12-12'},
    {'nombre_med': 'Ivermectina 634', 'presentacion': 'Tableta', 'stock_disponible': 39, 'fecha_vencimiento': '2027-05-09'},
    {'nombre_med': 'Enrofloxacina 769', 'presentacion': 'Jarabe', 'stock_disponible': 39, 'fecha_vencimiento': '2027-06-08'},
    {'nombre_med': 'Clindamicina 263', 'presentacion': 'Jarabe', 'stock_disponible': 27, 'fecha_vencimiento': '2027-01-09'},
    {'nombre_med': 'Prednisolona 981', 'presentacion': 'Tableta', 'stock_disponible': 62, 'fecha_vencimiento': '2026-01-08'},
    {'nombre_med': 'Prednisolona 983', 'presentacion': 'Jarabe', 'stock_disponible': 46, 'fecha_vencimiento': '2026-04-21'},
    {'nombre_med': 'Amoxicilina 440', 'presentacion': 'Crema', 'stock_disponible': 39, 'fecha_vencimiento': '2026-06-26'},
    {'nombre_med': 'Doxiciclina 384', 'presentacion': 'Solución oral', 'stock_disponible': 32, 'fecha_vencimiento': '2026-04-14'},
    {'nombre_med': 'Doxiciclina 322', 'presentacion': 'Inyectable', 'stock_disponible': 55, 'fecha_vencimiento': '2025-12-21'},
    {'nombre_med': 'Doxiciclina 960', 'presentacion': 'Solución oral', 'stock_disponible': 27, 'fecha_vencimiento': '2026-05-06'},
    {'nombre_med': 'Amoxicilina 730', 'presentacion': 'Solución oral', 'stock_disponible': 46, 'fecha_vencimiento': '2026-08-26'},
    {'nombre_med': 'Amoxicilina 853', 'presentacion': 'Inyectable', 'stock_disponible': 85, 'fecha_vencimiento': '2026-02-23'},
    {'nombre_med': 'Cefalexina 979', 'presentacion': 'Crema', 'stock_disponible': 97, 'fecha_vencimiento': '2026-06-03'},
]

for med in medicamentos_data:
    obj, creado = Medicamento.objects.get_or_create(
        nombre_med=med["nombre_med"],
        defaults=med
    )
    if creado:
        print(f"✓ Agregado: {obj.nombre_med}")
    else:
        print(f"- Ya existía: {obj.nombre_med}")
