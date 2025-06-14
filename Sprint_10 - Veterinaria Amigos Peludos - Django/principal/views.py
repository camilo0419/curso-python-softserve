from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from django.db import models
from conexion import crear_conexion  
from datetime import date
from .models import Cliente, Mascota, Consulta
from .forms import ClienteForm, MascotaForm, ConsultaForm

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

#ORM Clientes

def lista_clientes(request):
    clientes = Cliente.objects.filter(activo=True)
    return render(request, 'principal/lista_clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'principal/formulario_cliente.html', {'form': form})

def editar_cliente(request, cedula):
    cliente = get_object_or_404(Cliente, cedula=cedula)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'principal/formulario_cliente.html', {'form': form})

def eliminar_cliente(request, cedula):
    cliente = get_object_or_404(Cliente, cedula=cedula)
    cliente.activo = False
    cliente.save()
    return redirect('lista_clientes')

#ORM Mascotas

def lista_mascotas(request):
    mascotas = Mascota.objects.filter(activo=True)
    return render(request, 'principal/lista_mascotas.html', {'mascotas': mascotas})

def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_mascotas')
    else:
        form = MascotaForm()
    return render(request, 'principal/formulario_mascota.html', {'form': form, 'modo': 'Crear'})


def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('lista_mascotas')
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'principal/formulario_mascota.html', {'form': form, 'modo': 'Editar'})


def eliminar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    mascota.activo = False
    mascota.save()
    return redirect('lista_mascotas')

def buscar_clientes(request):
    q = request.GET.get('q', '').strip().lower()
    coincidencias = Cliente.objects.filter(
        activo=True
    ).filter(
        models.Q(nombre__icontains=q) | models.Q(cedula__icontains=q)
    ).values('id', 'nombre', 'cedula')[:10]

    return JsonResponse(list(coincidencias), safe=False)

def mascotas_por_cliente(request, cedula):
    cliente = get_object_or_404(Cliente, cedula=cedula, activo=True)
    mascotas = Mascota.objects.filter(cliente=cliente, activo=True)  # eliminación lógica
    return render(request, 'principal/mascotas_por_cliente.html', {
        'cliente': cliente,
        'mascotas': mascotas
    })


#ORM Consultas
def lista_consultas(request):
    consultas = Consulta.objects.select_related('mascota').order_by('-fecha')
    return render(request, 'principal/lista_consultas.html', {'consultas': consultas})

def crear_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = ConsultaForm()
    return render(request, 'principal/formulario_consulta.html', {'form': form})

def editar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'principal/formulario_consulta.html', {'form': form})

def eliminar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    consulta.delete()
    return redirect('lista_consultas')
