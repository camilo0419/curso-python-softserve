import openpyxl
from django.http import HttpResponse
from io import BytesIO

def generar_excel(nombre_archivo, encabezados, filas):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos"
    ws.append(encabezados)

    for fila in filas:
        ws.append(fila)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = f'attachment; filename={nombre_archivo}.xlsx'
    return response
