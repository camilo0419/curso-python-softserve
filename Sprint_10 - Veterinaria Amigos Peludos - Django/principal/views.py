from django.shortcuts import render
from conexion import crear_conexion  
from datetime import date

def inicio(request):
    fecha = request.GET.get('fecha', date.today().isoformat())
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT consultas.id, consultas.motivo, consultas.diagnostico, mascotas.nombre_mascota
        FROM consultas
        JOIN mascotas ON consultas.mascota_id = mascotas.id
        WHERE consultas.fecha = ?
    """, (fecha,))
    consultas = cursor.fetchall()
    conexion.close()

    return render(request, 'principal/inicio.html', {
        'consultas': consultas,
        'fecha': fecha
    })

def clientes(request):
    return render(request, 'principal/clientes.html')

def mascotas(request):
    return render(request, 'principal/mascotas.html')
